package com.ogheapsters.dumstigram

import okhttp3.MultipartBody
import okhttp3.OkHttpClient
import okhttp3.ResponseBody
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.*
import java.util.concurrent.TimeUnit

interface ApiService {

    companion object {
        val instance: ApiService by lazy {
            val okHttpClient = OkHttpClient.Builder()
                .readTimeout(20, TimeUnit.SECONDS)
                .connectTimeout(20, TimeUnit.SECONDS)
                .build()

            return@lazy Retrofit.Builder()
                .baseUrl("https://dumstigram.herokuapp.com")
                .addConverterFactory(GsonConverterFactory.create())
                .client(okHttpClient)
                .build()
                .create(ApiService::class.java)
        }
    }

    @Multipart
    @POST("/home?asApi=true")
    suspend fun submitImage(@Part file: MultipartBody.Part): ResponseBody

    @Multipart
    @POST("/filters/{selectedFilter}")
    suspend fun filterImage(@Part file: MultipartBody.Part, @Path("selectedFilter") filter: String): ResponseBody

    @GET("/filters")
    suspend fun fetchFilters(): List<String>

}