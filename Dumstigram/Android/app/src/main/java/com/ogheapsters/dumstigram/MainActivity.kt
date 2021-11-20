package com.ogheapsters.dumstigram

import android.content.res.Configuration.UI_MODE_NIGHT_YES
import android.graphics.drawable.Drawable
import android.net.Uri
import android.os.Bundle
import android.util.Log
import androidx.activity.ComponentActivity
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.compose.setContent
import androidx.activity.result.contract.ActivityResultContracts
import androidx.activity.viewModels
import androidx.appcompat.content.res.AppCompatResources
import androidx.compose.foundation.Image
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CornerSize
import androidx.compose.material.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.twotone.Image
import androidx.compose.material.icons.twotone.UploadFile
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Alignment.Companion.Center
import androidx.compose.ui.Alignment.Companion.CenterVertically
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.ColorFilter
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.core.graphics.drawable.toBitmap
import coil.annotation.ExperimentalCoilApi
import coil.compose.ImagePainter
import coil.compose.rememberImagePainter
import com.google.accompanist.drawablepainter.rememberDrawablePainter
import com.google.accompanist.systemuicontroller.rememberSystemUiController
import com.ogheapsters.dumstigram.ui.theme.DumstigramTheme
import com.ogheapsters.dumstigram.ui.theme.NavigationBarColor

class MainActivity : ComponentActivity() {

    private val viewModel by viewModels<MainViewModel>()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        setContent {
            DumstigramTheme {
                MainActivityContentView(viewModel)
            }
        }
    }
}

@OptIn(ExperimentalCoilApi::class)
@Composable
fun MainActivityContentView(viewModel: MainViewModel) {
    val systemUiController = rememberSystemUiController()
    val useDarkIcons = MaterialTheme.colors.isLight
    val navigationBarColor = NavigationBarColor

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

    val currentDrawable: MutableState<Drawable?> = remember { mutableStateOf(null) }

    Scaffold(
        floatingActionButton = {
            FloatingActionButton(
                onClick = {
                    viewModel.submitImage(currentDrawable?.value)
                },
                contentColor = MaterialTheme.colors.onPrimary,
                backgroundColor = MaterialTheme.colors.primary
            ) {
                Icon(
                    Icons.TwoTone.UploadFile,
                    contentDescription = "Floating action button icon",
                )
            }
        },
        isFloatingActionButtonDocked = true,
        bottomBar = {
            val launcher = rememberLauncherForActivityResult(
                contract = ActivityResultContracts.GetContent()
            ) { uri: Uri? ->
                viewModel.setImageUri(uri)
            }

            BottomAppBar(
                backgroundColor = MaterialTheme.colors.primary,
                cutoutShape = MaterialTheme.shapes.small.copy(
                    CornerSize(percent = 50)
                )
            ) {
                IconButton(onClick = { launcher.launch("image/*") }) {
                    Icon(
                        Icons.TwoTone.Image,
                        contentDescription = "Floating action button icon"
                    )
                }
            }
        },
        topBar = {
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
                            .align(Alignment.Center)
                            .offset(y = 4.dp),
                        contentDescription = "App Logo",
                        colorFilter = ColorFilter.tint(MaterialTheme.colors.onBackground),
                        contentScale = ContentScale.Fit,
                    )
                }

            }
        }
    ) { contentPadding ->
        Box(contentAlignment = Center) {
            val imagePainter = rememberImagePainter(
                data = viewModel.imageUri.value?.toString(),
                builder = {
                    crossfade(true)
                }
            )

            Image(
                painter = imagePainter,
                modifier = Modifier
                    .fillMaxSize()
                    .padding(
                        start = 0.dp,
                        top = contentPadding.calculateTopPadding() + 8.dp,
                        end = 0.dp,
                        bottom = contentPadding.calculateBottomPadding() + 48.dp
                    ),
                contentDescription = "Selected image view",
                contentScale = ContentScale.FillWidth,
            )

            when (val state = imagePainter.state) {
                ImagePainter.State.Empty -> {

                }
                is ImagePainter.State.Loading -> {
                    CircularProgressIndicator()
                }
                is ImagePainter.State.Success -> {
                    currentDrawable.value = state.result.drawable
                }
                is ImagePainter.State.Error -> {

                }
            }
        }
    }
}

@Preview(showSystemUi = false, uiMode = UI_MODE_NIGHT_YES)
@Composable
fun Preview() {
    val viewModel = MainViewModel()
    MainActivityContentView(viewModel)
}