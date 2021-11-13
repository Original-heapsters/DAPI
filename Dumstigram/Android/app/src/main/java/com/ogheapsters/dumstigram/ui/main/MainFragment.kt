package com.ogheapsters.dumstigram.ui.main

import android.app.Activity.RESULT_OK
import android.content.Intent
import androidx.lifecycle.ViewModelProvider
import android.os.Bundle
import android.provider.MediaStore
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import com.ogheapsters.dumstigram.R
import com.ogheapsters.dumstigram.databinding.MainFragmentBinding

class MainFragment : Fragment() {

    companion object {
        val TAG: String = MainFragment::class.java.simpleName
        fun newInstance() = MainFragment()
    }

    private val viewModel: MainViewModel by lazy {
        ViewModelProvider(this)[MainViewModel::class.java]
    }

    private var _viewBinding: MainFragmentBinding? = null
    private val viewBinding
        get() = _viewBinding!!

    private val imageSelectionResultCode = 69420

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _viewBinding = MainFragmentBinding.inflate(inflater, container, false)
        return viewBinding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        viewBinding.button.setOnClickListener {
            val gallery = Intent(Intent.ACTION_PICK, MediaStore.Images.Media.INTERNAL_CONTENT_URI)
            startActivityForResult(gallery, imageSelectionResultCode)
        }

        viewModel.imageUri.observe(viewLifecycleOwner, { uri ->
            viewBinding.imageView.setImageURI(uri)
        })
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        if (resultCode == RESULT_OK && requestCode == imageSelectionResultCode) {
            viewModel.setImageUri(data?.data)
        }

        viewBinding.imageView.setImageResource(R.drawable.ic_baseline_upload_24)
    }
}