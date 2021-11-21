package com.ogheapsters.dumstigram

import android.content.Context
import android.net.Uri
import android.provider.MediaStore

fun Uri.getSelectedImagePathForFile(context: Context): String {
    var result: String? = null
    val proj: Array<String> = arrayOf(MediaStore.Images.Media._ID)
    val cursor = context.contentResolver.query(this, proj, null, null, null)
    if (cursor != null) {
        if (cursor.moveToFirst()) {
            val columnIndex: Int = cursor.getColumnIndexOrThrow(proj[0])
            result = cursor.getString(columnIndex)
        }
        cursor.close()
    }
    if (result == null) {
        result = "Not found"
    }
    return result
}