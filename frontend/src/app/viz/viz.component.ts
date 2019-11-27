import { Component, OnInit } from '@angular/core';
import 'node_modules/leaflet-choropleth/dist/choropleth.js'
import { StoreService } from '../store.service';
import * as $ from 'jquery';
import Chart from 'chart.js';

declare let L;

@Component({
  selector: 'app-viz',
  templateUrl: './viz.component.html',
  styleUrls: ['./viz.component.scss']
})
export class VizComponent implements OnInit {

  geojsonData: any;
  myChart: any;
  map: any;
  year: number;
  week: number;
  median: number;
  medianPer: number;
  lineTrend: any;
  selectedDensity: any;
  showLineChart = false;
  max = 0;

  constructor(private store: StoreService) {

  }

  convertTOGeoJSON(polygons) {
    let features = [];
    let totalValues = [];

    for (var i = 0; i < polygons.result.length; i++) {
      let polygon = polygons.result[i];
      if (polygon.value > 0) {

        let properties = { density: polygon.value };
        let geometry = {
          "type": "Polygon",
          "coordinates": [[[polygon.lon1, polygon.lat1], [polygon.lon2, polygon.lat2], [polygon.lon3, polygon.lat3], [polygon.lon4, polygon.lat4]]]
        }

        var availableMonth = [];
        let trendValue = [];
        var monthList = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

        monthList.forEach((month) => {
          if (polygon[month.toLowerCase()]) {
            availableMonth.push(month)
            trendValue.push(polygon[month.toLowerCase()]);
          }
        });

        let montlyTrend = {
          labels: availableMonth,
          data: trendValue
        }

        features.push({
          "type": "Feature",
          properties,
          geometry,
          montlyTrend
        });


        this.max = this.max < polygon.value ? polygon.value : this.max;

        totalValues.push(polygon.value);
      }
    }

    this.computeMedian(totalValues);
    return {
      "type": "FeatureCollection",
      "features": features
    }

  }

  computeMedian(values) {
    let median;

    values.sort(function(a, b) {
      return a - b;
    });

    let half = Math.floor(values.length / 2);

    if (values.length % 2)
      median = values[half];

    median = (values[half - 1] + values[half]) / 2.0;

    this.median = median;
    let medianIndex = 0;
    values.forEach((value, index) => {
      if (value >= median) {
        medianIndex = index;
      }
    });

    if (medianIndex == 0) {
      this.medianPer = 100;
    } else {
      this.medianPer = (values.length / (medianIndex)) * 10;
    }

  }

  ngOnInit() {
    this.map = L.map('mapid').setView([32.00118, -87.359296], 4);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
      minZoom: 3,
      maxZoom: 6
    }).addTo(this.map);


    const formData = new FormData();
    let dateStr = $("#date").val();
    formData.append('past_year', dateStr.substring(0, 4));
    formData.append('past_week', dateStr.substring(dateStr.length - 2, dateStr.length));

    this.store.post('/visualise_past_data', formData).subscribe((res) => {

      this.geojsonData = this.convertTOGeoJSON(res);
      this.initMap();
    });
  }

  initMap() {
    var map = this.map;
    var info = L.control();

    info.onAdd = function(map) {
      $(".info").remove();
      this._div = L.DomUtil.create('div', 'info'); // create a div with a class "info"
      this.update();
      return this._div;
    };

    // method that we will use to update the control based on feature properties passed
    info.update = function(props) {
      this._div.innerHTML = '<h6>Fishing Vessel Density Range</h6><div class="chartreport"></div>';
    };

    info.addTo(map);

    var geojsonLayer;

    geojsonLayer = L.choropleth(this.geojsonData, {
      valueProperty: 'density', // which property in the features to use
      scale: ['white', 'blue'], // chroma.js scale - include as many as you like
      mode: 'q', // q for quantile, e for equidistant, k for k-means
      style: {
        color: '#fff', // border color
        weight: 0,
        fillOpacity: 0.9
      },
      onEachFeature: ((feature, layer) => {
        layer.on({
          mouseover: ((e) => {
            var layer = e.target;

            layer.setStyle({
              weight: 2,
              fillOpacity: 1
            });

            if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
              layer.bringToFront();
            }
          }),
          mouseout: ((e) => {
            geojsonLayer.resetStyle(e.target);
          }),
          click: ((e) => {
            this.showLineChart = false;
            this.selectedDensity = feature.properties.density;
            this.lineTrend = feature.montlyTrend;

            setTimeout(() => {
              this.showLineChart = true;
              $('html, body').animate({
                scrollTop: $("#scroll-to").offset().top
              }, 1000);
              console.log(feature.montlyTrend)
            }, 300);
          })
        });
      })
    }).addTo(map)

    if (this.myChart == undefined) {
      info.update();
    }


    this.drawDoughnut();
  }

  drawDoughnut() {
    $("canvas#doughchartContainer").remove();

    $("div.chartreport").append('<canvas id="doughchartContainer" style="height: 170px; width: 210px;"></canvas>');

    var ctx = $("#doughchartContainer");
    let per = this.medianPer;
    let doughColor = '#ffc107';

    if (per < 25) {
      doughColor = "#28a745";
    }
    else if (per > 70) {
      doughColor = "#dc3545";
    }

    if (this.myChart != undefined) {
      this.myChart.destroy();
    }

    this.myChart = new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: ['Median', 'Max'],
        datasets: [{
          label: '# of Votes',
          data: [this.median, this.max],
          backgroundColor: [
            doughColor
          ],
          //cutoutPercentage : ,
          borderWidth: 5
        }]
      }
    });
  }

  submitQuery(e) {
    e.preventDefault();

    const formData = new FormData();
    let dateStr = $("#date").val();
    formData.append('past_year', dateStr.substring(0, 4));
    formData.append('past_week', dateStr.substring(dateStr.length - 2, dateStr.length));

    this.store.post('/visualise_past_data', formData).subscribe((res) => {

      this.geojsonData = this.convertTOGeoJSON(res);
      this.initMap();
    });
  }


}
