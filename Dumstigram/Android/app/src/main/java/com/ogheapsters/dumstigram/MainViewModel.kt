package com.ogheapsters.dumstigram

import android.graphics.drawable.Drawable
import android.net.Uri
import android.util.Log
import androidx.compose.runtime.MutableState
import androidx.compose.runtime.State
import androidx.compose.runtime.mutableStateOf
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.launch
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.MultipartBody
import okhttp3.RequestBody.Companion.toRequestBody
import java.util.*
import android.graphics.Bitmap

import android.graphics.drawable.BitmapDrawable
import androidx.core.graphics.drawable.toBitmap
import java.io.ByteArrayOutputStream


class MainViewModel : ViewModel() {

    private val _imageUri: MutableState<Uri?> = mutableStateOf(null)
    val imageUri: State<Uri?>
        get() = _imageUri

    var movieListResponse: MutableState<String> = mutableStateOf("")
    var errorMessage: MutableState<String> = mutableStateOf("")

    fun setImageUri(uri: Uri?) {
        _imageUri.value = uri
    }

    fun submitImage(drawable: Drawable?) {
        if (drawable == null) return

        viewModelScope.launch {
            val apiService = ApiService.getInstance()

            val stream = ByteArrayOutputStream()
            drawable.toBitmap().compress(Bitmap.CompressFormat.JPEG, 100, stream)
            val bitmapByteArray: ByteArray = stream.toByteArray()

            val requestFile = bitmapByteArray.toRequestBody("image/*".toMediaTypeOrNull(), 0, bitmapByteArray.size)
            val body = MultipartBody.Part.createFormData("image", UUID.randomUUID().toString(), requestFile)

            try {
                val submitImageRequest = apiService.submitImage(body)
                Log.d("RESPONSE", submitImageRequest)
                movieListResponse.value = submitImageRequest
            } catch (e: Exception) {
                errorMessage.value = e.message.toString()
            }
        }
    }
}