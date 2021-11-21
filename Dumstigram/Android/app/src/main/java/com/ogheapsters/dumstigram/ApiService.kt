package com.ogheapsters.dumstigram

import okhttp3.MultipartBody
import okhttp3.OkHttpClient
import okhttp3.ResponseBody
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.Multipart
import retrofit2.http.POST
import retrofit2.http.Part
import java.util.concurrent.TimeUnit


interface ApiService {

    companion object {
        var apiService: ApiService? = null
        fun getInstance(): ApiService {
            if (apiService == null) {
                val okHttpClient = OkHttpClient.Builder()
                    .readTimeout(20, TimeUnit.SECONDS)
                    .connectTimeout(20, TimeUnit.SECONDS)
                    .build()

                apiService = Retrofit.Builder()
                    .baseUrl("https://dumstigram.herokuapp.com/")
                    .addConverterFactory(GsonConverterFactory.create())
                    .client(okHttpClient)
                    .build().create(ApiService::class.java)
            }
            return apiService!!
        }
    }

    @Multipart
    @POST("home?asApi=true")
    suspend fun submitImage(@Part file: MultipartBody.Part): ResponseBody

}