package com.ogheapsters.dumstigram

import android.content.Context
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.graphics.drawable.Drawable
import androidx.compose.runtime.Composable
import androidx.core.graphics.drawable.toBitmap
import androidx.lifecycle.ViewModel
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.MultipartBody
import okhttp3.RequestBody.Companion.asRequestBody
import java.io.*
import java.util.*

class MainViewModel : ViewModel() {

    fun saveBitmapToCache(context: Context, name: String, bitmap: Bitmap): File? {
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
            return null
        }
        try {
            fos.write(bitmapByteArray)
            fos.flush()
            fos.close()
        } catch (e: IOException) {
            e.printStackTrace()
        }
        return tempFile
    }

    suspend fun dumbifyImage(someFile: File?, context: Context): File? = withContext(Dispatchers.IO) {
        val file = someFile ?: return@withContext null
        val apiService = ApiService.getInstance()
        val requestFile = file.asRequestBody("multipart/form-data".toMediaTypeOrNull())
        val body = MultipartBody.Part.createFormData(
            "file",
            UUID.randomUUID().toString() + ".jpg",
            requestFile
        )
        val submitImageResponse = apiService.submitImage(body)
        val bufferedInputStream = BufferedInputStream(submitImageResponse.byteStream())
        val bitmap = BitmapFactory.decodeStream(bufferedInputStream)
        val cachedImageFile = saveBitmapToCache(context, UUID.randomUUID().toString(), bitmap)
        return@withContext cachedImageFile
    }
}