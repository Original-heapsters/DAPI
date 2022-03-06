/*
   Licensed to the Apache Software Foundation (ASF) under one or more
   contributor license agreements.  See the NOTICE file distributed with
   this work for additional information regarding copyright ownership.
   The ASF licenses this file to You under the Apache License, Version 2.0
   (the "License"); you may not use this file except in compliance with
   the License.  You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
*/
var showControllersOnly = false;
var seriesFilter = "";
var filtersOnlySampleSeries = true;

/*
 * Add header in statistics table to group metrics by category
 * format
 *
 */
function summaryTableHeader(header) {
    var newRow = header.insertRow(-1);
    newRow.className = "tablesorter-no-sort";
    var cell = document.createElement('th');
    cell.setAttribute("data-sorter", false);
    cell.colSpan = 1;
    cell.innerHTML = "Requests";
    newRow.appendChild(cell);

    cell = document.createElement('th');
    cell.setAttribute("data-sorter", false);
    cell.colSpan = 3;
    cell.innerHTML = "Executions";
    newRow.appendChild(cell);

    cell = document.createElement('th');
    cell.setAttribute("data-sorter", false);
    cell.colSpan = 6;
    cell.innerHTML = "Response Times (ms)";
    newRow.appendChild(cell);

    cell = document.createElement('th');
    cell.setAttribute("data-sorter", false);
    cell.colSpan = 1;
    cell.innerHTML = "Throughput";
    newRow.appendChild(cell);

    cell = document.createElement('th');
    cell.setAttribute("data-sorter", false);
    cell.colSpan = 2;
    cell.innerHTML = "Network (KB/sec)";
    newRow.appendChild(cell);
}

/*
 * Populates the table identified by id parameter with the specified data and
 * format
 *
 */
function createTable(table, info, formatter, defaultSorts, seriesIndex, headerCreator) {
    var tableRef = table[0];

    // Create header and populate it with data.titles array
    var header = tableRef.createTHead();

    // Call callback is available
    if(headerCreator) {
        headerCreator(header);
    }

    var newRow = header.insertRow(-1);
    for (var index = 0; index < info.titles.length; index++) {
        var cell = document.createElement('th');
        cell.innerHTML = info.titles[index];
        newRow.appendChild(cell);
    }

    var tBody;

    // Create overall body if defined
    if(info.overall){
        tBody = document.createElement('tbody');
        tBody.className = "tablesorter-no-sort";
        tableRef.appendChild(tBody);
        var newRow = tBody.insertRow(-1);
        var data = info.overall.data;
        for(var index=0;index < data.length; index++){
            var cell = newRow.insertCell(-1);
            cell.innerHTML = formatter ? formatter(index, data[index]): data[index];
        }
    }

    // Create regular body
    tBody = document.createElement('tbody');
    tableRef.appendChild(tBody);

    var regexp;
    if(seriesFilter) {
        regexp = new RegExp(seriesFilter, 'i');
    }
    // Populate body with data.items array
    for(var index=0; index < info.items.length; index++){
        var item = info.items[index];
        if((!regexp || filtersOnlySampleSeries && !info.supportsControllersDiscrimination || regexp.test(item.data[seriesIndex]))
                &&
                (!showControllersOnly || !info.supportsControllersDiscrimination || item.isController)){
            if(item.data.length > 0) {
                var newRow = tBody.insertRow(-1);
                for(var col=0; col < item.data.length; col++){
                    var cell = newRow.insertCell(-1);
                    cell.innerHTML = formatter ? formatter(col, item.data[col]) : item.data[col];
                }
            }
        }
    }

    // Add support of columns sort
    table.tablesorter({sortList : defaultSorts});
}

$(document).ready(function() {

    // Customize table sorter default options
    $.extend( $.tablesorter.defaults, {
        theme: 'blue',
        cssInfoBlock: "tablesorter-no-sort",
        widthFixed: true,
        widgets: ['zebra']
    });

    var data = {"OkPercent": 100.0, "KoPercent": 0.0};
    var dataset = [
        {
            "label" : "KO",
            "data" : data.KoPercent,
            "color" : "#FF6347"
        },
        {
            "label" : "OK",
            "data" : data.OkPercent,
            "color" : "#9ACD32"
        }];
    $.plot($("#flot-requests-summary"), dataset, {
        series : {
            pie : {
                show : true,
                radius : 1,
                label : {
                    show : true,
                    radius : 3 / 4,
                    formatter : function(label, series) {
                        return '<div style="font-size:8pt;text-align:center;padding:2px;color:white;">'
                            + label
                            + '<br/>'
                            + Math.round10(series.percent, -2)
                            + '%</div>';
                    },
                    background : {
                        opacity : 0.5,
                        color : '#000'
                    }
                }
            }
        },
        legend : {
            show : true
        }
    });

    // Creates APDEX table
    createTable($("#apdexTable"), {"supportsControllersDiscrimination": true, "overall": {"data": [1.0, 500, 1500, "Total"], "isController": false}, "titles": ["Apdex", "T (Toleration threshold)", "F (Frustration threshold)", "Label"], "items": [{"data": [1.0, 500, 1500, "Test Isolated Route - brightness"], "isController": false}, {"data": [1.0, 500, 1500, "Test Isolated Route - arrow_face"], "isController": false}, {"data": [1.0, 500, 1500, "Test Isolated Route - arrow"], "isController": false}, {"data": [1.0, 500, 1500, "Test Isolated Route - grayscale"], "isController": false}, {"data": [1.0, 500, 1500, "Test Isolated Route - bulge"], "isController": false}, {"data": [1.0, 500, 1500, "Test Isolated Route - circle_smile"], "isController": false}, {"data": [1.0, 500, 1500, "Test Isolated Route - emoji_overlay"], "isController": false}, {"data": [1.0, 500, 1500, "Test Isolated Route - noise"], "isController": false}, {"data": [1.0, 500, 1500, "Test Isolated Route - sharpen"], "isController": false}, {"data": [1.0, 500, 1500, "Test Isolated Route - laser_eyes"], "isController": false}, {"data": [1.0, 500, 1500, "Test Isolated Route - mustache"], "isController": false}, {"data": [1.0, 500, 1500, "Test Isolated Route - circle"], "isController": false}, {"data": [1.0, 500, 1500, "Test Isolated Route - black_and_white"], "isController": false}, {"data": [1.0, 500, 1500, "Test Isolated Route - swirl"], "isController": false}, {"data": [1.0, 500, 1500, "Test Isolated Route - inpaint"], "isController": false}]}, function(index, item){
        switch(index){
            case 0:
                item = item.toFixed(3);
                break;
            case 1:
            case 2:
                item = formatDuration(item);
                break;
        }
        return item;
    }, [[0, 0]], 3);

    // Create statistics table
    createTable($("#statisticsTable"), {"supportsControllersDiscrimination": true, "overall": {"data": ["Total", 1000, 0, 0.0, 41.568999999999996, 5, 311, 92.0, 151.0, 225.98000000000002, 23.902287448908858, 3726.9933947522527, 577.9530622564954], "isController": false}, "titles": ["Label", "#Samples", "KO", "Error %", "Average", "Min", "Max", "90th pct", "95th pct", "99th pct", "Transactions\/s", "Received", "Sent"], "items": [{"data": ["Test Isolated Route - brightness", 67, 0, 0.0, 7.985074626865675, 6, 15, 11.0, 12.599999999999994, 15.0, 1.6224331654397521, 50.183289922147424, 39.23245725221571], "isController": false}, {"data": ["Test Isolated Route - arrow_face", 67, 0, 0.0, 26.238805970149254, 23, 41, 29.0, 31.599999999999994, 41.0, 1.621530046709746, 295.57305847491466, 39.2089879202062], "isController": false}, {"data": ["Test Isolated Route - arrow", 67, 0, 0.0, 60.02985074626866, 53, 104, 66.0, 81.79999999999993, 104.0, 1.618474768703046, 295.54173045450153, 39.127703245404255], "isController": false}, {"data": ["Test Isolated Route - grayscale", 67, 0, 0.0, 9.940298507462686, 7, 42, 12.0, 13.0, 42.0, 1.6220011136127048, 107.85673811339481, 39.223333628380175], "isController": false}, {"data": ["Test Isolated Route - bulge", 67, 0, 0.0, 33.10447761194032, 28, 60, 40.0, 41.599999999999994, 60.0, 1.6214123227336528, 300.6892940276971, 39.19829517266831], "isController": false}, {"data": ["Test Isolated Route - circle_smile", 67, 0, 0.0, 29.328358208955216, 25, 38, 33.0, 35.0, 38.0, 1.621530046709746, 296.0405057298095, 39.21421119067499], "isController": false}, {"data": ["Test Isolated Route - emoji_overlay", 67, 0, 0.0, 20.253731343283587, 14, 28, 25.0, 27.0, 28.0, 1.6218048024786986, 284.53561559746566, 39.21981563316954], "isController": false}, {"data": ["Test Isolated Route - noise", 66, 0, 0.0, 33.10606060606061, 22, 59, 52.300000000000004, 54.65, 59.0, 1.620466989123229, 517.8635961170173, 39.17526420824228], "isController": false}, {"data": ["Test Isolated Route - sharpen", 66, 0, 0.0, 9.272727272727272, 6, 23, 13.0, 14.649999999999999, 23.0, 1.6212232866617537, 159.72865907485874, 39.20009672070744], "isController": false}, {"data": ["Test Isolated Route - laser_eyes", 66, 0, 0.0, 85.46969696969698, 59, 116, 106.30000000000001, 112.3, 116.0, 1.619592157247675, 295.79697334881354, 39.16324522711099], "isController": false}, {"data": ["Test Isolated Route - mustache", 66, 0, 0.0, 43.56060606060608, 39, 73, 48.0, 58.149999999999984, 73.0, 1.620705743682931, 296.2187945080176, 39.18715122596567], "isController": false}, {"data": ["Test Isolated Route - circle", 67, 0, 0.0, 60.731343283582085, 54, 76, 68.0, 70.19999999999999, 76.0, 1.6203927638579858, 295.77302522189706, 39.180189149112415], "isController": false}, {"data": ["Test Isolated Route - black_and_white", 67, 0, 0.0, 6.507462686567165, 5, 13, 8.0, 9.0, 13.0, 1.6224724542922873, 5.071810865419542, 39.2448768010655], "isController": false}, {"data": ["Test Isolated Route - swirl", 66, 0, 0.0, 15.545454545454541, 13, 30, 18.300000000000004, 21.299999999999997, 30.0, 1.6208251473477406, 298.58091463040273, 39.18672872666994], "isController": false}, {"data": ["Test Isolated Route - inpaint", 67, 0, 0.0, 182.14925373134332, 120, 311, 233.4, 253.39999999999998, 311.0, 1.6132139073485505, 294.48464154898636, 39.00254058617452], "isController": false}]}, function(index, item){
        switch(index){
            // Errors pct
            case 3:
                item = item.toFixed(2) + '%';
                break;
            // Mean
            case 4:
            // Mean
            case 7:
            // Percentile 1
            case 8:
            // Percentile 2
            case 9:
            // Percentile 3
            case 10:
            // Throughput
            case 11:
            // Kbytes/s
            case 12:
            // Sent Kbytes/s
                item = item.toFixed(2);
                break;
        }
        return item;
    }, [[0, 0]], 0, summaryTableHeader);

    // Create error table
    createTable($("#errorsTable"), {"supportsControllersDiscrimination": false, "titles": ["Type of error", "Number of errors", "% in errors", "% in all samples"], "items": []}, function(index, item){
        switch(index){
            case 2:
            case 3:
                item = item.toFixed(2) + '%';
                break;
        }
        return item;
    }, [[1, 1]]);

        // Create top5 errors by sampler
    createTable($("#top5ErrorsBySamplerTable"), {"supportsControllersDiscrimination": false, "overall": {"data": ["Total", 1000, 0, null, null, null, null, null, null, null, null, null, null], "isController": false}, "titles": ["Sample", "#Samples", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors"], "items": [{"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}]}, function(index, item){
        return item;
    }, [[0, 0]], 0);

});
