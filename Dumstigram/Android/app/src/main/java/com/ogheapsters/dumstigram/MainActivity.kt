package com.ogheapsters.dumstigram

import android.content.Context
import android.content.Intent
import android.content.res.Configuration.UI_MODE_NIGHT_YES
import android.graphics.drawable.Drawable
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.compose.setContent
import androidx.activity.result.contract.ActivityResultContracts
import androidx.activity.viewModels
import androidx.appcompat.content.res.AppCompatResources
import androidx.compose.foundation.Image
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.foundation.shape.CornerSize
import androidx.compose.material.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.twotone.Error
import androidx.compose.material.icons.twotone.Image
import androidx.compose.material.icons.twotone.Send
import androidx.compose.material.icons.twotone.Share
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Alignment.Companion.BottomStart
import androidx.compose.ui.Alignment.Companion.Center
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.ColorFilter
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.core.content.FileProvider
import androidx.core.graphics.drawable.toBitmap
import androidx.lifecycle.lifecycleScope
import androidx.lifecycle.viewModelScope
import coil.annotation.ExperimentalCoilApi
import coil.compose.ImagePainter
import coil.compose.rememberImagePainter
import coil.request.CachePolicy
import com.google.accompanist.drawablepainter.rememberDrawablePainter
import com.google.accompanist.systemuicontroller.rememberSystemUiController
import com.ogheapsters.dumstigram.ui.theme.DumstigramTheme
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import java.io.*
import java.util.*


sealed class MainActivityState {
    object Empty : MainActivityState()
    object Loading : MainActivityState()
    data class ImageSelected(val file: File?) : MainActivityState()
    object ImageSent : MainActivityState()
    data class ImageReceived(val file: File?) : MainActivityState()
    data class Error(val exception: Throwable) : MainActivityState()
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
    val viewState: MutableState<MainActivityState> =
        remember { mutableStateOf(MainActivityState.Empty) }

    SideEffect {
        systemUiController.setSystemBarsColor(
            color = Color.Transparent,
            darkIcons = useDarkIcons
        )
//        systemUiController.setNavigationBarColor(
//            color = navigationBarColor,
//            darkIcons = useDarkIcons
//        )
    }

    Scaffold(
        bottomBar = { BottomNavigationBar(viewState, viewModel) },
        topBar = { TopToolbar() }
    ) { contentPadding ->
        Box(
            contentAlignment = Center, modifier = Modifier
                .fillMaxSize()
                .padding(contentPadding)
        ) {
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
                    MainImageView(imagePainter)

                    FilterList(
                        modifier = Modifier
                            .align(BottomStart),
                        viewModel = viewModel
                    )
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

                    MainImageView(imagePainter)
                    FilterList(
                        modifier = Modifier
                            .align(BottomStart),
                        viewModel = viewModel
                    )
                }
                is MainActivityState.Error -> {
                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                        Icon(
                            Icons.TwoTone.Error,
                            contentDescription = null,
                            tint = MaterialTheme.colors.error
                        )
                        Spacer(modifier = Modifier.height(8.dp))
                        Text(text = state.exception.localizedMessage ?: "Unknown error")
                    }
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
        Box(modifier = Modifier.fillMaxSize()) {
            Image(
                painter = rememberDrawablePainter(drawable = drawable),
                modifier = Modifier
                    .width(164.dp)
                    .align(BottomStart),
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
        Drawable.createFromStream(inputStream, uri.toString())?.run {
            val randomFileName = UUID.randomUUID().toString()
            when (val savedBitmapResult = viewModel.saveBitmapToCache(context, randomFileName, this.toBitmap())) {
                is Result.Success -> {
                    viewState.value = MainActivityState.ImageSelected(savedBitmapResult.value)
                }
                is Result.Failure -> {
                    viewState.value = MainActivityState.Error(savedBitmapResult.reason)
                }
            }
        }
    }

    fun shareImage(file: File, context: Context) {
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
        if (viewState.value != MainActivityState.Loading && viewState.value != MainActivityState.ImageSent) {
            SelectImageButton {
                launcher.launch("image/*")
            }
        }

        when (val state = viewState.value) {
            is MainActivityState.ImageSelected -> {
                ShareImageButton {
                    state.file?.let { file ->
                        shareImage(file, context)
                    }
                }
                SendImageButton {
                    viewState.value = MainActivityState.ImageSent
                    state.file?.let { file ->
                        viewModel.viewModelScope.launch {
                            when (val dumbImageResult = viewModel.dumbifyImage(file, context)) {
                                is Result.Success -> {
                                    viewState.value =
                                        MainActivityState.ImageReceived(dumbImageResult.value)
                                }
                                is Result.Failure -> {
                                    viewState.value =
                                        MainActivityState.Error(dumbImageResult.reason)
                                }
                            }
                        }
                    }
                }
            }

            is MainActivityState.ImageReceived -> {
                ShareImageButton {
                    state.file?.let { file ->
                        shareImage(file, context)
                    }
                }
                SendImageButton {
                    viewState.value = MainActivityState.ImageSent
                    state.file?.let { file ->
                        viewModel.viewModelScope.launch {
                            when (val dumbImageResult = viewModel.dumbifyImage(file, context)) {
                                is Result.Success -> {
                                    viewState.value =
                                        MainActivityState.ImageReceived(dumbImageResult.value)
                                }
                                is Result.Failure -> {
                                    viewState.value =
                                        MainActivityState.Error(dumbImageResult.reason)
                                }
                            }
                        }
                    }
                }
            }
            else -> {}
        }
    }
}

@Composable
fun SelectImageButton(onClick: () -> Unit) {
    IconButton(onClick = onClick) {
        Icon(
            Icons.TwoTone.Image,
            contentDescription = null
        )
    }
}

@Composable
fun ShareImageButton(onClick: () -> Unit) {
    IconButton(onClick = onClick) {
        Icon(
            Icons.TwoTone.Share,
            contentDescription = null
        )
    }
}

@Composable
fun SendImageButton(onClick: () -> Unit) {
    IconButton(onClick = onClick) {
        Icon(
            Icons.TwoTone.Send,
            contentDescription = null
        )
    }
}

@Composable
fun MainImageView(painter: ImagePainter) {
    Image(
        painter = painter,
        modifier = Modifier.fillMaxSize(),
        contentDescription = null,
        contentScale = ContentScale.FillWidth,
    )
}

@Composable
fun FilterList(viewModel: MainViewModel, modifier: Modifier) {
    val listState = rememberLazyListState()

    LazyRow(
        modifier = modifier
            .fillMaxWidth()
            .offset(y = -(8.dp)), state = listState
    ) {
        items(viewModel.filterList) { filter ->
            Chip(name = filter, isSelected = viewModel.selectedFilter == filter) {
                viewModel.selectedFilter = filter
            }
        }
    }
}

@Preview(showSystemUi = false, uiMode = UI_MODE_NIGHT_YES)
@Composable
fun Preview() {
    val viewModel = MainViewModel()
    val scope = CoroutineScope(Dispatchers.Main)
    MainActivityContentView(viewModel, scope)
}