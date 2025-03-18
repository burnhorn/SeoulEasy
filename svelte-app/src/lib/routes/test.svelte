<script>
  import { onMount, afterUpdate } from 'svelte';
  import Plotly from 'plotly.js-dist';

  export let place = ''; // 외부에서 전달받을 관광지 이름

  let regionData = [];
  // let selectedRegion = 'POI016'; // 기본 region_id
  let areaCongest = '';
  let congestionMessage = '';

  let _url = import.meta.env.VITE_SERVER_URL

  async function fetchRegionData(regionId) {
    const response = await fetch(`${_url}/populations/region/${regionId}`);
    const data = await response.json();
    regionData = data;

    // area_congest와 congestion_message는 첫 번째 데이터 기준으로 설정
    if (regionData.length > 0) {
      areaCongest = regionData[0].area_congest;
      congestionMessage = regionData[0].congestion_message;
    }

    updateCharts();
  }

  function updateCharts() {
    if (regionData.length === 0) return;

    // X축 데이터 (datetime)
    const dates = regionData.map(d => d.datetime);

    // 왼쪽 차트: male_rate와 female_rate
    const maleRate = regionData.map(d => d.male_rate);
    const femaleRate = regionData.map(d => d.female_rate);
    const leftChartData = [
      { x: dates, y: maleRate, type: 'scatter', mode: 'lines+markers', name: 'Male Rate' },
      { x: dates, y: femaleRate, type: 'scatter', mode: 'lines+markers', name: 'Female Rate' }
    ];
    Plotly.newPlot('left-chart', leftChartData, {
      title: 'Male vs Female Rate',
      xaxis: { title: 'Time', type: 'date', tickformat: '%H:%M' },
      yaxis: { title: 'Rate (%)' }
    });

    // 가운데 차트: gen_10 ~ gen_70
    const gen10 = regionData.map(d => d.gen_10);
    const gen20 = regionData.map(d => d.gen_20);
    const gen30 = regionData.map(d => d.gen_30);
    const gen40 = regionData.map(d => d.gen_40);
    const gen50 = regionData.map(d => d.gen_50);
    const gen60 = regionData.map(d => d.gen_60);
    const gen70 = regionData.map(d => d.gen_70);
    const centerChartData = [
      { x: dates, y: gen10, type: 'scatter', mode: 'lines+markers', name: 'Gen 10' },
      { x: dates, y: gen20, type: 'scatter', mode: 'lines+markers', name: 'Gen 20' },
      { x: dates, y: gen30, type: 'scatter', mode: 'lines+markers', name: 'Gen 30' },
      { x: dates, y: gen40, type: 'scatter', mode: 'lines+markers', name: 'Gen 40' },
      { x: dates, y: gen50, type: 'scatter', mode: 'lines+markers', name: 'Gen 50' },
      { x: dates, y: gen60, type: 'scatter', mode: 'lines+markers', name: 'Gen 60' },
      { x: dates, y: gen70, type: 'scatter', mode: 'lines+markers', name: 'Gen 70' }
    ];
    Plotly.newPlot('center-chart', centerChartData, {
      title: 'Generation Distribution',
      xaxis: { title: 'Time', type: 'date', tickformat: '%H:%M' },
      yaxis: { title: 'Percentage (%)' }
    });

    // 오른쪽 차트: min_population과 max_population
    const minPopulation = regionData.map(d => d.min_population);
    const maxPopulation = regionData.map(d => d.max_population);
    const rightChartData = [
      { x: dates, y: minPopulation, type: 'scatter', mode: 'lines+markers', name: 'Min Population' },
      { x: dates, y: maxPopulation, type: 'scatter', mode: 'lines+markers', name: 'Max Population' }
    ];
    Plotly.newPlot('right-chart', rightChartData, {
      title: 'Population Range',
      xaxis: { title: 'Time', type: 'date', tickformat: '%H:%M' },
      yaxis: { title: 'Population' }
    });
  }

  onMount(() => {
    fetchRegionData(place);
  });

  afterUpdate(() => {
    fetchRegionData(place);
  });
</script>

<div class="charts-container">
  <div id="left-chart" class="chart"></div>
  <div id="center-chart" class="chart"></div>
  <div id="right-chart" class="chart"></div>
</div>

<div class="info">
  <p><strong>Area Congestion:</strong> {areaCongest}</p>
  <p><strong>Congestion Message:</strong> {congestionMessage}</p>
</div>

<style>
  .charts-container {
    display: flex;
    justify-content: space-between;
    gap: 20px;
    margin-bottom: 20px;
  }

  .chart {
    width: 30%; /* 각 차트의 너비 */
    height: 400px; /* 차트 높이 */
  }

  .info {
    text-align: center;
    font-size: 16px;
    margin-top: 20px;
  }
</style>