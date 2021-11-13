package com.ogheapsters.dumstigram.ui.main

import android.net.Uri
import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel

class MainViewModel : ViewModel() {

    private val _imageUri = MutableLiveData<Uri?>()
    val imageUri: LiveData<Uri?>
        get() = _imageUri

    fun setImageUri(uri: Uri?) {
        _imageUri.postValue(uri)
    }
}