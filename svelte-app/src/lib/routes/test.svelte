<script>
  import { onMount, afterUpdate, onDestroy } from 'svelte';
  import Plotly from 'plotly.js-dist';

  export let place = ''; // 외부에서 전달받을 관광지 이름
  export let gptResponse = ''; // GPT API 결과를 저장할 변수
  let regionData = [];
  let areaCongest = '';
  let congestionMessage = '';
  

  // 환경 변수에서 서버 URL을 가져옵니다.
  let _url = import.meta.env.VITE_SERVER_URL;

  // regionData를 가져오는 API 호출 함수
  async function fetchRegionData(regionId) {
    try {
      const response = await fetch(`${_url}/populations/region/${regionId}`);
      const data = await response.json();
      regionData = data;

      // 첫 번째 데이터 기준으로 congestion 값 설정
      if (regionData.length > 0) {
        areaCongest = regionData[0].area_congest;
        congestionMessage = regionData[0].congestion_message;
      }
      updateCharts();
    } catch (error) {
      console.error('데이터 수집 오류:', error);
    }
  }

  // Plotly 차트 업데이트 함수
  function updateCharts() {
    if (regionData.length === 0) return;

    // X축 데이터 (datetime)
    const dates = regionData.map(d => d.datetime);

    // 왼쪽 차트: male_rate와 female_rate
    const leftChartData = [
      { x: dates, y: regionData.map(d => d.male_rate), type: 'scatter', mode: 'lines+markers', name: 'Male Rate' },
      { x: dates, y: regionData.map(d => d.female_rate), type: 'scatter', mode: 'lines+markers', name: 'Female Rate' }
    ];
    Plotly.newPlot('left-chart', leftChartData, {
      title: 'Male vs Female Rate',
      xaxis: { title: 'Time', type: 'date', tickformat: '%H:%M:%S' }, // x축에 datetime 표시
      yaxis: { title: 'Rate (%)' },
      responsive: true
    });

    // 가운데 차트: Generation Distribution
    const centerChartData = [
      { x: dates, y: regionData.map(d => d.gen_10), type: 'scatter', mode: 'lines+markers', name: 'Gen 10' },
      { x: dates, y: regionData.map(d => d.gen_20), type: 'scatter', mode: 'lines+markers', name: 'Gen 20' },
      { x: dates, y: regionData.map(d => d.gen_30), type: 'scatter', mode: 'lines+markers', name: 'Gen 30' },
      { x: dates, y: regionData.map(d => d.gen_40), type: 'scatter', mode: 'lines+markers', name: 'Gen 40' },
      { x: dates, y: regionData.map(d => d.gen_50), type: 'scatter', mode: 'lines+markers', name: 'Gen 50' },
      { x: dates, y: regionData.map(d => d.gen_60), type: 'scatter', mode: 'lines+markers', name: 'Gen 60' },
      { x: dates, y: regionData.map(d => d.gen_70), type: 'scatter', mode: 'lines+markers', name: 'Gen 70' }
    ];
    Plotly.newPlot('center-chart', centerChartData, {
      title: 'Generation Distribution',
      xaxis: { title: 'Time', type: 'date', tickformat: '%H:%M:%S' }, // x축에 datetime 표시
      yaxis: { title: 'Percentage (%)' },
      responsive: true
    });

    // 오른쪽 차트: Population Range
    const rightChartData = [
      { x: dates, y: regionData.map(d => d.min_population), type: 'scatter', mode: 'lines+markers', name: 'Min Population' },
      { x: dates, y: regionData.map(d => d.max_population), type: 'scatter', mode: 'lines+markers', name: 'Max Population' }
    ];
    Plotly.newPlot('right-chart', rightChartData, {
      title: 'Population Range',
      xaxis: { title: 'Time', type: 'date', tickformat: '%H:%M:%S' }, // x축에 datetime 표시
      yaxis: { title: 'Population' },
      responsive: true
    });
  }

  // 창 크기 변경 시 차트를 재조정하는 함수
  function handleResize() {
    Plotly.Plots.resize(document.getElementById('left-chart'));
    Plotly.Plots.resize(document.getElementById('center-chart'));
    Plotly.Plots.resize(document.getElementById('right-chart'));
  }

  // 컴포넌트가 마운트될 때 데이터 가져오기 및 리사이즈 이벤트 등록
  onMount(() => {
    fetchRegionData(place);
    window.addEventListener('resize', handleResize);
  });

  // place 값이 변경될 때마다 데이터 다시 가져오기
  let previousPlace = place;
  afterUpdate(() => {
    if (place !== previousPlace) {
      fetchRegionData(place);
      previousPlace = place;
    }
  });

  // 컴포넌트가 파괴될 때 리사이즈 이벤트 제거
  onDestroy(() => {
    window.removeEventListener('resize', handleResize);
  });
</script>

<!-- 정보 영역 -->
<div class="info">
  <div class="info-item">
    <p><strong>🚦 Area Congestion:</strong> {areaCongest}</p>
  </div>
  <div class="info-item">
    <p><strong>💬 Congestion Message:</strong> {congestionMessage}</p>
  </div>
  <div class="info-item">
    <p><strong>🤖 GPT Response:</strong> {gptResponse}</p>
  </div>
</div>

<!-- 차트 컨테이너 -->
<div class="charts-container">
  <div id="left-chart" class="chart"></div>
  <div id="center-chart" class="chart"></div>
  <div id="right-chart" class="chart"></div>
</div>

<style>
  .info {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin-bottom: 20px;
    padding: 10px;
    background-color: #f9f9f9;
    border-radius: 5px;
  }
  .info-item {
    display: flex;
    align-items: center;
  }
  .charts-container {
    display: flex;
    flex-direction: column;
    gap: 40px;
    margin-bottom: 50px;
    overflow-y: auto;
  }
  .chart {
    width: 100%;
    height: 70vw;
    max-height: 500px;
  }
  /* 태블릿 이상 */
  @media (min-width: 768px) {
    .charts-container {
      flex-direction: row;
      justify-content: space-between;
    }
    .chart {
      width: 45%;
      height: 300px;
    }
  }
  /* 데스크톱 이상 */
  @media (min-width: 1024px) {
    .charts-container {
      gap: 20px;
    }
    .chart {
      width: 100%;
      height: 400px;
    }
  }
</style>
