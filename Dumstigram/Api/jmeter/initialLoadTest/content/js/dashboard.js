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
    createTable($("#apdexTable"), {"supportsControllersDiscrimination": true, "overall": {"data": [0.9815, 500, 1500, "Total"], "isController": false}, "titles": ["Apdex", "T (Toleration threshold)", "F (Frustration threshold)", "Label"], "items": [{"data": [1.0, 500, 1500, "Test Isolated Route - brightness"], "isController": false}, {"data": [1.0, 500, 1500, "Test Isolated Route - arrow_face"], "isController": false}, {"data": [1.0, 500, 1500, "Test Isolated Route - arrow"], "isController": false}, {"data": [1.0, 500, 1500, "Test Isolated Route - grayscale"], "isController": false}, {"data": [1.0, 500, 1500, "Test Isolated Route - bulge"], "isController": false}, {"data": [1.0, 500, 1500, "Test Isolated Route - circle_smile"], "isController": false}, {"data": [1.0, 500, 1500, "Test Isolated Route - emoji_overlay"], "isController": false}, {"data": [1.0, 500, 1500, "Test Isolated Route - noise"], "isController": false}, {"data": [1.0, 500, 1500, "Test Isolated Route - sharpen"], "isController": false}, {"data": [1.0, 500, 1500, "Test Isolated Route - laser_eyes"], "isController": false}, {"data": [1.0, 500, 1500, "Test Isolated Route - mustache"], "isController": false}, {"data": [1.0, 500, 1500, "Test Isolated Route - circle"], "isController": false}, {"data": [1.0, 500, 1500, "Test Isolated Route - black_and_white"], "isController": false}, {"data": [1.0, 500, 1500, "Test Isolated Route - swirl"], "isController": false}, {"data": [0.7238805970149254, 500, 1500, "Test Isolated Route - inpaint"], "isController": false}]}, function(index, item){
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
    createTable($("#statisticsTable"), {"supportsControllersDiscrimination": true, "overall": {"data": ["Total", 1000, 0, 0.0, 69.056, 6, 931, 96.0, 409.4999999999993, 784.7300000000002, 14.420234473012531, 2260.7298091932603, 348.67984724916005], "isController": false}, "titles": ["Label", "#Samples", "KO", "Error %", "Average", "Min", "Max", "90th pct", "95th pct", "99th pct", "Transactions\/s", "Received", "Sent"], "items": [{"data": ["Test Isolated Route - brightness", 67, 0, 0.0, 10.014925373134327, 7, 16, 13.200000000000003, 15.0, 16.0, 0.9785593269848688, 32.215095007886895, 23.66235698154612], "isController": false}, {"data": ["Test Isolated Route - arrow_face", 67, 0, 0.0, 28.597014925373138, 26, 35, 32.0, 33.0, 35.0, 0.9781593085727635, 178.40531974494863, 23.654010133803435], "isController": false}, {"data": ["Test Isolated Route - arrow", 67, 0, 0.0, 64.07462686567166, 57, 95, 72.4, 79.79999999999998, 95.0, 0.9771606918881077, 178.4407399212073, 23.62466284765773], "isController": false}, {"data": ["Test Isolated Route - grayscale", 67, 0, 0.0, 11.940298507462686, 8, 43, 13.200000000000003, 14.0, 43.0, 0.9787880558639631, 65.08558232411033, 23.667916363838895], "isController": false}, {"data": ["Test Isolated Route - bulge", 67, 0, 0.0, 39.6865671641791, 32, 55, 46.2, 47.599999999999994, 55.0, 0.9782164340360918, 181.5674241608509, 23.650272910522396], "isController": false}, {"data": ["Test Isolated Route - circle_smile", 67, 0, 0.0, 31.40298507462686, 28, 37, 34.0, 35.599999999999994, 37.0, 0.9784450026286582, 178.68265717641947, 23.662059745385246], "isController": false}, {"data": ["Test Isolated Route - emoji_overlay", 67, 0, 0.0, 21.179104477611936, 16, 35, 27.0, 27.0, 35.0, 0.9786164991820518, 170.91066164790985, 23.66682045034617], "isController": false}, {"data": ["Test Isolated Route - noise", 66, 0, 0.0, 37.757575757575765, 26, 71, 57.0, 58.0, 71.0, 0.9796936230851443, 305.9934827412496, 23.68368455256947], "isController": false}, {"data": ["Test Isolated Route - sharpen", 66, 0, 0.0, 11.212121212121213, 7, 18, 16.0, 16.0, 18.0, 0.9799991090917191, 114.65383457132464, 23.696115709497086], "isController": false}, {"data": ["Test Isolated Route - laser_eyes", 66, 0, 0.0, 90.93939393939392, 65, 122, 109.0, 113.65, 122.0, 0.9786186649269001, 178.72941402427273, 23.663649181889625], "isController": false}, {"data": ["Test Isolated Route - mustache", 66, 0, 0.0, 46.69696969696968, 42, 71, 50.0, 56.949999999999996, 71.0, 0.9793737943315031, 179.0016021479448, 23.681300081614484], "isController": false}, {"data": ["Test Isolated Route - circle", 67, 0, 0.0, 64.38805970149255, 59, 75, 67.2, 70.0, 75.0, 0.9779736968865405, 178.55616198692871, 23.645359323227606], "isController": false}, {"data": ["Test Isolated Route - black_and_white", 67, 0, 0.0, 7.492537313432836, 6, 10, 9.0, 10.0, 10.0, 0.9785593269848688, 3.0589535211704737, 23.66687836836186], "isController": false}, {"data": ["Test Isolated Route - swirl", 66, 0, 0.0, 19.575757575757574, 16, 29, 23.0, 25.949999999999996, 29.0, 0.9798681631925886, 181.0225529741226, 23.68912186275165], "isController": false}, {"data": ["Test Isolated Route - inpaint", 67, 0, 0.0, 548.8059701492535, 261, 931, 809.4, 837.1999999999998, 931.0, 0.9706909291105863, 176.7324727808122, 23.47064961588891], "isController": false}]}, function(index, item){
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
