package com.ogheapsters.dumstigram

import android.content.Context
import android.content.Intent
import android.content.res.Configuration.UI_MODE_NIGHT_YES
import android.graphics.Bitmap
import android.graphics.drawable.Drawable
import android.net.Uri
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.compose.setContent
import androidx.activity.result.contract.ActivityResultContracts
import androidx.activity.viewModels
import androidx.appcompat.content.res.AppCompatResources
import androidx.compose.foundation.Image
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CornerSize
import androidx.compose.material.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.twotone.Image
import androidx.compose.material.icons.twotone.SendToMobile
import androidx.compose.material.icons.twotone.Share
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Alignment.Companion.Center
import androidx.compose.ui.Alignment.Companion.CenterVertically
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.ColorFilter
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.core.graphics.drawable.toBitmap
import androidx.core.net.toUri
import androidx.lifecycle.lifecycleScope
import coil.annotation.ExperimentalCoilApi
import coil.compose.ImagePainter
import coil.compose.rememberImagePainter
import coil.request.CachePolicy
import com.google.accompanist.drawablepainter.rememberDrawablePainter
import com.google.accompanist.systemuicontroller.rememberSystemUiController
import com.ogheapsters.dumstigram.ui.theme.DumstigramTheme
import com.ogheapsters.dumstigram.ui.theme.NavigationBarColor
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import java.io.*
import java.util.*
import androidx.core.content.FileProvider


sealed class MainActivityState {
    object Empty : MainActivityState()
    object Loading : MainActivityState()
    data class ImageSelected(val file: File?) : MainActivityState()
    object ImageSent : MainActivityState()
    data class ImageReceived(val file: File?) : MainActivityState()
}

class MainActivity : ComponentActivity() {

    private val viewModel by viewModels<MainViewModel>()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            DumstigramTheme {
                MainActivityContentView(viewModel, lifecycleScope)
            }
        }
    }
}

@OptIn(ExperimentalCoilApi::class)
@Composable
fun MainActivityContentView(viewModel: MainViewModel, lifecycleScope: CoroutineScope) {
    val systemUiController = rememberSystemUiController()
    val useDarkIcons = MaterialTheme.colors.isLight
    val navigationBarColor = NavigationBarColor
    val viewState: MutableState<MainActivityState> =
        remember { mutableStateOf(MainActivityState.Empty) }

    SideEffect {
        systemUiController.setSystemBarsColor(
            color = Color.Transparent,
            darkIcons = useDarkIcons
        )
        systemUiController.setNavigationBarColor(
            color = navigationBarColor,
            darkIcons = useDarkIcons
        )
    }

    Scaffold(
        floatingActionButton = {
            val context = LocalContext.current
            when (val state = viewState.value) {
                is MainActivityState.ImageSelected -> {
                    SendImageButton {
                        lifecycleScope.launch {
                            val dumbBitmapFile = viewModel.dumbifyImage(state.file, context)
                            viewState.value = MainActivityState.ImageReceived(dumbBitmapFile)
                        }
                        viewState.value = MainActivityState.ImageSent
                    }
                }
                is MainActivityState.ImageReceived -> {
                    SendImageButton {
                        lifecycleScope.launch {
                            val dumbBitmap = viewModel.dumbifyImage(state.file, context)
                            viewState.value = MainActivityState.ImageReceived(dumbBitmap)
                        }
                        viewState.value = MainActivityState.ImageSent
                    }
                }
                else -> {}
            }
        },
        isFloatingActionButtonDocked = true,
        bottomBar = { BottomNavigationBar(viewState, viewModel) },
        topBar = { TopToolbar() }
    ) { contentPadding ->
        Box(contentAlignment = Center, modifier = Modifier.fillMaxSize()) {
            when (val state = viewState.value) {
                MainActivityState.Empty -> {
                    Text(text = "Choose an image", modifier = Modifier.offset(y = (-40).dp))
                }
                MainActivityState.Loading -> {
                    CircularProgressIndicator()
                }
                is MainActivityState.ImageSelected -> {
                    val imagePainter = rememberImagePainter(
                        data = state.file,
                        builder = {
                            crossfade(true)
                            diskCachePolicy(CachePolicy.DISABLED)
                        }
                    )

                    MainImageView(imagePainter, contentPadding)
                }
                MainActivityState.ImageSent -> {
                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                        CircularProgressIndicator()
                        Spacer(modifier = Modifier.height(4.dp))
                        Text(text = "Sometimes it takes a while")
                    }
                }
                is MainActivityState.ImageReceived -> {
                    val imagePainter = rememberImagePainter(
                        data = state.file,
                        builder = {
                            crossfade(true)
                            diskCachePolicy(CachePolicy.DISABLED)
                        }
                    )

                    MainImageView(imagePainter, contentPadding)
                }
            }
        }
    }
}

@Composable
fun TopToolbar() {
    TopAppBar(
        backgroundColor = Color.Transparent,
        elevation = 0.dp
    ) {
        val drawable = AppCompatResources.getDrawable(
            LocalContext.current,
            R.drawable.ic_logo
        )
        Box(
            modifier = Modifier
                .fillMaxSize()
                .align(CenterVertically)
        ) {
            Image(
                painter = rememberDrawablePainter(drawable = drawable),
                modifier = Modifier
                    .width(164.dp)
                    .align(Center)
                    .offset(y = 4.dp),
                contentDescription = "App Logo",
                colorFilter = ColorFilter.tint(MaterialTheme.colors.onBackground),
                contentScale = ContentScale.Fit,
            )
        }
    }
}

@Composable
fun BottomNavigationBar(viewState: MutableState<MainActivityState>, viewModel: MainViewModel) {
    val context = LocalContext.current

    val launcher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.GetContent()
    ) {
        val uri = it ?: return@rememberLauncherForActivityResult
        val inputStream = context.contentResolver.openInputStream(uri)
        val drawable = Drawable.createFromStream(inputStream, uri.toString())
        viewModel.saveBitmapToCache(context, UUID.randomUUID().toString(), drawable.toBitmap())
            ?.let { file ->
                viewState.value = MainActivityState.ImageSelected(file)
            }
    }

    fun shareImage(context: Context, file: File) {
        val contentUri =
            FileProvider.getUriForFile(context, "com.ogheapsters.dumstigram.fileprovider", file)

        val shareIntent: Intent = Intent().apply {
            action = Intent.ACTION_SEND
            putExtra(Intent.EXTRA_STREAM, contentUri)
            type = "image/jpg"
        }
        context.startActivity(Intent.createChooser(shareIntent, "Send to"))
    }

    BottomAppBar(
        backgroundColor = MaterialTheme.colors.primary,
        cutoutShape = MaterialTheme.shapes.small.copy(
            CornerSize(percent = 50)
        )
    ) {
        BottomBarButtonItem(Icons.TwoTone.Image) {
            launcher.launch("image/*")
        }

        when (val state = viewState.value) {
            is MainActivityState.ImageReceived -> {
                BottomBarButtonItem(Icons.TwoTone.Share) {
                    state.file?.let { file ->
                        shareImage(context, file)
                    }
                }
            }
            is MainActivityState.ImageSelected -> {
                BottomBarButtonItem(Icons.TwoTone.Share) {
                    state.file?.let { file ->
                        shareImage(context, file)
                    }
                }
            }
            else -> {}
        }
    }
}

@Composable
fun BottomBarButtonItem(imageVector: ImageVector, onClick: () -> Unit) {
    IconButton(onClick = onClick) {
        Icon(
            imageVector,
            contentDescription = null
        )
    }
}

@Composable
fun SendImageButton(onClick: () -> Unit) {
    FloatingActionButton(
        onClick = { onClick() },
        contentColor = MaterialTheme.colors.onPrimary,
        backgroundColor = MaterialTheme.colors.primary,
    ) {
        Icon(
            Icons.TwoTone.SendToMobile,
            contentDescription = null,
        )
    }
}

@Composable
fun MainImageView(painter: ImagePainter, contentPadding: PaddingValues) {
    Image(
        painter = painter,
        modifier = Modifier
            .fillMaxSize()
            .padding(
                start = 0.dp,
                top = contentPadding.calculateTopPadding() + 8.dp,
                end = 0.dp,
                bottom = contentPadding.calculateBottomPadding() + 48.dp
            ),
        contentDescription = null,
        contentScale = ContentScale.FillWidth,
    )
}

@Preview(showSystemUi = false, uiMode = UI_MODE_NIGHT_YES)
@Composable
fun Preview() {
    val viewModel = MainViewModel()
    val scope = CoroutineScope(Dispatchers.Main)
    MainActivityContentView(viewModel, scope)
}