// -------------------- script.js --------------------
let currentData = [];
let sentimentChart = null, scoreBarChart = null, topWordsChart = null;

const landingPage = document.getElementById('landing-page');
const dashboardPage = document.getElementById('dashboard-page');
const textInput = document.getElementById('textInput');
const fileInput = document.getElementById('fileInput');
const attachBtn = document.getElementById('attachBtn');
const filesCount = document.getElementById('filesCount');
const analyzeBtn = document.getElementById('analyzeBtn');
const errorMsg = document.getElementById('errorMessage');
const resetBtn = document.getElementById('resetBtn');
const newAnalysisBtn = document.getElementById('newAnalysisBtn');
const searchInput = document.getElementById('searchInput');
const exportBtn = document.getElementById('exportBtn');
const exportFilteredBtn = document.getElementById('exportFilteredBtn');

const POSITIVE_WORDS = new Set(["good","great","excellent","amazing","love","nice","outstanding",
    "fantastic","wonderful","perfect","brilliant","awesome","best","happy","satisfied",
    "recommend","fast","friendly","helpful","superb","positive","enjoy","liked","cool","fine"]);

const NEGATIVE_WORDS = new Set(["bad","poor","terrible","hate","worst","disappointing","awful","horrible",
    "useless","broken","defective","unhappy","garbage","junk","slow","fail","failed",
    "issue","problem","difficult","error","bug","delay","waste","cheap","annoying","hard"]);

// --------- File Upload ---------
attachBtn.addEventListener('click',()=>fileInput.click());
fileInput.addEventListener('change',function(){ filesCount.textContent = `${this.files.length} file(s) uploaded`; });

// --------- Reset / New Analysis ---------
resetBtn.addEventListener('click',resetDashboard);
newAnalysisBtn.addEventListener('click',resetDashboard);

function resetDashboard(){
    textInput.value = "";
    fileInput.value = "";
    searchInput.value = "";
    filesCount.textContent = "0 files uploaded";
    currentData = [];
    destroyCharts();
    dashboardPage.classList.add('hidden');
    landingPage.classList.remove('hidden');
    // Switch back to dark theme for landing
    document.body.classList.add('bg-gray-900','text-gray-100');
    document.body.classList.remove('bg-white','text-gray-900');
}

// --------- Analyze ---------
analyzeBtn.addEventListener('click', async ()=>{
    const textValue = textInput.value.trim();
    const files = fileInput.files;
    if(!textValue && files.length===0){
        errorMsg.textContent = "Provide text or upload files"; errorMsg.classList.remove('hidden'); return;
    }
    errorMsg.classList.add('hidden');
    analyzeBtn.disabled = true; analyzeBtn.textContent = "Processing...";

    const formData = new FormData();
    if(textValue) formData.append('raw_text', textValue);
    Array.from(files).forEach(f => formData.append('files', f));

    try{
        const res = await fetch('/api/process',{method:'POST', body: formData});
        if(!res.ok) throw new Error("Server error or large file");
        const data = await res.json();
        currentData = data.data;

        // Update metrics
        document.getElementById("metric-total").textContent = data.metrics.total;
        document.getElementById("metric-positive").textContent = data.metrics.positive;
        document.getElementById("metric-negative").textContent = data.metrics.negative;
        document.getElementById("metric-neutral").textContent = data.metrics.neutral;

        document.getElementById("performanceInfo").textContent =
            `⏱ Normal: ${data.performance.normal_time}s | ⚡ Parallel: ${data.performance.parallel_time}s | 🧠 Cores: ${data.performance.cores} | 📦 Chunks: ${data.performance.chunks}`;

        renderTable(currentData);
        renderCharts(currentData);
        renderTopWordsChart(currentData);

        // Switch to dashboard (light theme)
        landingPage.classList.add('hidden');
        dashboardPage.classList.remove('hidden');
        document.body.classList.remove('bg-gray-900','text-gray-100');
        document.body.classList.add('bg-white','text-gray-900');

    }catch(err){ 
        errorMsg.textContent = err.message; 
        errorMsg.classList.remove('hidden'); 
    }finally{
        analyzeBtn.disabled = false; analyzeBtn.textContent = "Analyze";
    }
});

// --------- Search (debounced) ---------
let debounceTimer = null;
searchInput.addEventListener('input',()=>{
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(()=>{
        const term = searchInput.value.toLowerCase();
        const filtered = currentData.filter(r => r.Text.toLowerCase().includes(term));
        renderTable(filtered);
    }, 200);
});

// --------- Table + Charts ---------
function renderTable(data){
    const tbody = document.getElementById('resultsTableBody');
    tbody.innerHTML = "";
    if(!data.length){ tbody.innerHTML='<tr><td colspan="3" class="p-4 text-center">No Data</td></tr>'; return; }
    data.forEach(r=>{
        const cls = r.Sentiment==='Positive'?'text-green-500':r.Sentiment==='Negative'?'text-red-500':'text-yellow-500';
        tbody.innerHTML += `<tr><td class="px-4 py-2">${r.Text}</td><td class="px-4 py-2 text-center">${r.Score}</td><td class="px-4 py-2 text-center ${cls}">${r.Sentiment}</td></tr>`;
    });
}

function destroyCharts(){
    if(sentimentChart) sentimentChart.destroy();
    if(scoreBarChart) scoreBarChart.destroy();
    if(topWordsChart) topWordsChart.destroy();
}

function renderCharts(data){
    destroyCharts();
    const pos = data.filter(r=>r.Sentiment==='Positive').length;
    const neg = data.filter(r=>r.Sentiment==='Negative').length;
    const neu = data.filter(r=>r.Sentiment==='Neutral').length;

    sentimentChart = new Chart(document.getElementById('sentimentChart'),{
        type:'doughnut', data:{labels:['Positive','Negative','Neutral'], datasets:[{data:[pos,neg,neu], backgroundColor:['#16a34a','#dc2626','#eab308']}]}
    });

    const counts = {};
    data.forEach(r => counts[r.Score]=(counts[r.Score]||0)+1);
    scoreBarChart = new Chart(document.getElementById('scoreBarChart'),{
        type:'bar', data:{labels:Object.keys(counts), datasets:[{data:Object.values(counts), backgroundColor:'#7c3aed'}]}
    });
}

function renderTopWordsChart(data){
    const wordCounts = {};
    data.forEach(r => {
        const words = r.Text.toLowerCase().match(/\b\w+\b/g);
        if(words) words.forEach(w=>wordCounts[w]=(wordCounts[w]||0)+1);
    });
    const top = Object.entries(wordCounts).sort((a,b)=>b[1]-a[1]).slice(0,10);
    topWordsChart = new Chart(document.getElementById('topWordsChart'),{
        type:'bar', data:{labels:top.map(x=>x[0]), datasets:[{data:top.map(x=>x[1]), backgroundColor:'#f97316'}]}, options:{indexAxis:'y', responsive:true}
    });
}

// --------- CSV Export Functions ---------
exportBtn.addEventListener('click',()=>{ exportCSV(currentData,'results.csv'); });

exportFilteredBtn.addEventListener('click',()=>{
    const term = searchInput.value.trim().toLowerCase();
    if(!term){ alert("Enter search term to download filtered CSV"); return; }
    const filteredData = currentData.filter(r => r.Text.toLowerCase().includes(term));
    if(!filteredData.length){ alert("No matching records found"); return; }
    exportCSV(filteredData, `filtered_results_${term}.csv`);
});

function exportCSV(data, filename){
    const csv = ['Text,Score,Positive,Negative,Sentiment,Keywords'];
    data.forEach(r=>{
        const words = String(r.Text).toLowerCase().match(/\b\w+\b/g)||[];
        const keywords = words.filter(w=>POSITIVE_WORDS.has(w)||NEGATIVE_WORDS.has(w));
        csv.push(`"${r.Text.replace(/"/g,'""')}",${r.Score},${r.Positive},${r.Negative},${r.Sentiment},"${keywords.join(' ')}"`);
    });
    const blob = new Blob([csv.join('\n')]);
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = filename;
    a.click();
}