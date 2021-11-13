package com.ogheapsters.dumstigram.ui.main

import androidx.lifecycle.ViewModelProvider
import android.os.Bundle
import android.util.Log
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
            Log.d(TAG, "Upload Image")
        }

        viewBinding.imageView.setImageResource(R.drawable.ic_baseline_upload_24)
    }
}