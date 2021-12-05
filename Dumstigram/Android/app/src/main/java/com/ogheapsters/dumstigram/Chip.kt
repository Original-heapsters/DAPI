package com.ogheapsters.dumstigram

import android.content.res.Configuration.UI_MODE_NIGHT_YES
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.selection.toggleable
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.MaterialTheme
import androidx.compose.material.Surface
import androidx.compose.material.Text
import androidx.compose.material.primarySurface
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp

@Preview(showBackground = true, uiMode = UI_MODE_NIGHT_YES)
@Composable
fun Chip(
    name: String = "Chip",
    isSelected: Boolean = true,
    onSelectionChanged: (String) -> Unit = {},
) {
    Surface(
        modifier = Modifier.padding(4.dp),
        elevation = 1.dp,
        shape = RoundedCornerShape(16.dp),
        color = if (isSelected) MaterialTheme.colors.primary else Color.DarkGray
    ) {
        Row(modifier = Modifier
            .toggleable(
                value = isSelected,
                onValueChange = {
                    onSelectionChanged(name)
                }
            )
        ) {
            Text(
                text = name,
                style = MaterialTheme.typography.body2,
                color = if (isSelected) MaterialTheme.colors.onPrimary else Color.Gray,
                modifier = Modifier.padding(8.dp)
            )
        }
    }
}