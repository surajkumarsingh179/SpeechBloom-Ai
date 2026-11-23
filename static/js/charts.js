/**
 * SpeechBloom AI — Chart.js Helpers v2
 */

function renderProgressChart(canvasId, weeklyData) {
  const ctx = document.getElementById(canvasId);
  if (!ctx || !window.Chart) return null;

  const labels        = weeklyData.map(d => d.date);
  const sessionCounts = weeklyData.map(d => d.sessions_count);
  const avgScores     = weeklyData.map(d => d.avg_score);

  return new Chart(ctx, {
    type: 'line',
    data: {
      labels,
      datasets: [
        {
          label: 'Pronunciation Score (%)',
          data: avgScores,
          borderColor: '#6C63FF',
          backgroundColor: 'rgba(108,99,255,0.08)',
          borderWidth: 3,
          fill: true,
          tension: 0.4,
          pointBackgroundColor: '#6C63FF',
          pointBorderColor: '#fff',
          pointBorderWidth: 2,
          pointRadius: 5,
          pointHoverRadius: 7,
          yAxisID: 'y'
        },
        {
          label: 'Sessions',
          data: sessionCounts,
          borderColor: '#4ECDC4',
          backgroundColor: 'rgba(78,205,196,0.55)',
          type: 'bar',
          borderRadius: 6,
          yAxisID: 'y1'
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      interaction: { mode: 'index', intersect: false },
      plugins: {
        legend: {
          position: 'top',
          labels: {
            font: { family: 'Nunito', weight: '700', size: 13 },
            usePointStyle: true,
            padding: 20
          }
        },
        tooltip: {
          backgroundColor: 'rgba(10,10,30,0.88)',
          titleFont: { family: 'Nunito', weight: '800', size: 13 },
          bodyFont: { family: 'Nunito', size: 12 },
          padding: 12,
          cornerRadius: 10
        }
      },
      scales: {
        x: {
          grid: { display: false },
          ticks: { font: { family: 'Nunito', weight: '700', size: 12 } }
        },
        y: {
          beginAtZero: true,
          max: 100,
          position: 'left',
          grid: { color: 'rgba(108,99,255,0.07)' },
          ticks: { font: { family: 'Nunito', weight: '700', size: 12 }, callback: v => `${v}%` },
          title: { display: true, text: 'Score (%)', font: { family: 'Nunito', weight: '800', size: 12 } }
        },
        y1: {
          beginAtZero: true,
          position: 'right',
          grid: { drawOnChartArea: false },
          ticks: { font: { family: 'Nunito', weight: '700', size: 12 }, stepSize: 1 },
          title: { display: true, text: 'Sessions', font: { family: 'Nunito', weight: '800', size: 12 } }
        }
      }
    }
  });
}
