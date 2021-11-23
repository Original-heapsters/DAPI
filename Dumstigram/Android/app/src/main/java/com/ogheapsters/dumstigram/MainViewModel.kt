package com.ogheapsters.dumstigram

import android.content.Context
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.MultipartBody
import okhttp3.RequestBody.Companion.asRequestBody
import java.io.*
import java.util.*

class MainViewModel : ViewModel() {

    private var apiService: ApiService = ApiService.instance

    var filterList by mutableStateOf<List<String>>(listOf())
        private set

    var selectedFilter by mutableStateOf<String?>(null)

    init {
        viewModelScope.launch {
            when (val listFromServer = fetchFilters()) {
                is Result.Success -> {
                    filterList = listFromServer.value
                }
                is Result.Failure -> {

                }
            }
        }
    }

    fun saveBitmapToCache(context: Context, name: String, bitmap: Bitmap): Result<File, Throwable> {
        val cacheDirectoryPath = context.cacheDir.path + "/image"
        val cacheDirectory = File(cacheDirectoryPath)
        cacheDirectory.mkdir()

        val tempFile = File(cacheDirectory, "${name}.jpg")
        tempFile.createNewFile()

        val outputStream = ByteArrayOutputStream()
        bitmap.compress(Bitmap.CompressFormat.JPEG, 100, outputStream)
        val bitmapByteArray: ByteArray = outputStream.toByteArray()

        val fos: FileOutputStream = try {
            FileOutputStream(tempFile)
        } catch (e: FileNotFoundException) {
            e.printStackTrace()
            return Result.Failure(e)
        }
        try {
            fos.write(bitmapByteArray)
            fos.flush()
            fos.close()
        } catch (e: IOException) {
            e.printStackTrace()
            return Result.Failure(e)
        }
        return Result.Success(tempFile)
    }

    private suspend fun fetchFilters(): Result<List<String>, Throwable> = withContext(Dispatchers.IO) {
        try {
            val response = apiService.fetchFilters()
            return@withContext Result.Success(response)
        } catch(e: Throwable) {
            return@withContext Result.Failure(e)
        }
    }

    suspend fun dumbifyImage(file: File, context: Context): Result<File, Throwable> = withContext(Dispatchers.IO) {
        val requestFile = file.asRequestBody("multipart/form-data".toMediaTypeOrNull())
        val body = MultipartBody.Part.createFormData(
            "file",
            UUID.randomUUID().toString() + ".jpg",
            requestFile
        )

        val bitmap: Bitmap
        try {
            val submitImageResponse = if (selectedFilter != null) apiService.filterImage(body, selectedFilter!!) else apiService.submitImage(body)
            val bufferedInputStream = BufferedInputStream(submitImageResponse.byteStream())
            bitmap = BitmapFactory.decodeStream(bufferedInputStream)
        } catch(error: Exception) {
            return@withContext Result.Failure(error)
        }

        try {
            when (val cachedImageFile = saveBitmapToCache(context, UUID.randomUUID().toString(), bitmap)) {
                is Result.Success -> {
                    return@withContext Result.Success(cachedImageFile.value)
                }
                is Result.Failure -> {
                    return@withContext Result.Failure(cachedImageFile.reason)
                }
            }
        } catch(error: Exception) {
            return@withContext Result.Failure(error)
        }
    }
}