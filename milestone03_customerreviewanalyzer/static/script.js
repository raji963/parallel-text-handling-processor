let currentData = [], filteredData = [];
let sentimentChart = null, scoreBarChart = null, topWordsChart = null;

const landingPage = document.getElementById('landing-page');
const dashboardPage = document.getElementById('dashboard-page');
const textInput = document.getElementById('textInput');
const fileInput = document.getElementById('fileInput');
const attachBtn = document.getElementById('attachBtn');
const filesCount = document.getElementById('filesCount');
const analyzeBtn = document.getElementById('analyzeBtn');
const resetBtn = document.getElementById('resetBtn');
const newAnalysisBtn = document.getElementById('newAnalysisBtn');
const searchInput = document.getElementById('searchInput');
const errorMsg = document.getElementById('errorMessage');

// The two export buttons
const exportFullBtn = document.getElementById('exportFullBtn');
const exportFilteredBtn = document.getElementById('exportFilteredBtn');

// ---------------- FILE UPLOAD ----------------
attachBtn.addEventListener('click', () => fileInput.click());
fileInput.addEventListener('change', function () {
    if (this.files && this.files.length > 0) {
        filesCount.textContent = `${this.files.length} file(s) uploaded`;
    }
});

// ---------------- RESET ----------------
function resetDashboard() {
    textInput.value = "";
    fileInput.value = "";
    searchInput.value = "";
    filesCount.textContent = "0 files uploaded";

    currentData = [];
    filteredData = [];
    destroyCharts();

    dashboardPage.classList.add('hidden');
    landingPage.classList.remove('hidden');

    document.body.classList.add('bg-gray-900','text-gray-100');
    document.body.classList.remove('bg-white','text-gray-900');
}

resetBtn.addEventListener('click', resetDashboard);
newAnalysisBtn.addEventListener('click', resetDashboard);

// ---------------- ANALYZE ----------------
analyzeBtn.addEventListener('click', async () => {
    const textValue = textInput.value.trim();
    const files = fileInput.files;
    if (!textValue && files.length === 0) {
        errorMsg.textContent = "Provide text or upload files"; errorMsg.classList.remove('hidden'); return;
    }
    errorMsg.classList.add('hidden');
    analyzeBtn.disabled = true; analyzeBtn.textContent = "Processing...";

    const formData = new FormData();
    if (textValue) formData.append('raw_text', textValue);
    Array.from(files).forEach(f => formData.append('files', f));

    try {
        const res = await fetch('/api/process', { method:'POST', body:formData });
        if (!res.ok) throw new Error("Server error or large file");

        const data = await res.json();
        currentData = filteredData = data.data;

        renderTable(filteredData);
        renderCharts(filteredData);
        renderTopWordsChart(filteredData);
        updateMetrics(filteredData);

        // Switch page
        landingPage.classList.add('hidden'); dashboardPage.classList.remove('hidden');
        document.body.classList.remove('bg-gray-900','text-gray-100');
        document.body.classList.add('bg-white','text-gray-900');

        document.getElementById('performanceInfo').textContent =
            `⏱ Normal: ${data.performance.normal_time}s |⚡ Parallel: ${data.performance.parallel_time}s |🧠  Cores: ${data.performance.cores} |📦 Records: ${data.metrics.total}`;

    } catch(err){
        errorMsg.textContent = err.message; errorMsg.classList.remove('hidden');
    } finally {
        analyzeBtn.disabled = false; analyzeBtn.textContent = "Analyze";
    }
});

// ---------------- SEARCH ----------------
let debounceTimer = null;
searchInput.addEventListener('input', () => {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
        const term = searchInput.value.trim().toLowerCase();
        filteredData = term ? currentData.filter(r => r.Text.toLowerCase().includes(term)) : currentData;
        renderTable(filteredData);
        renderCharts(filteredData);
        renderTopWordsChart(filteredData);
        updateMetrics(filteredData);
    }, 200); // 200ms debounce prevents lagging when typing fast
});

// ---------------- METRICS ----------------
function updateMetrics(data){
    let pos = 0, neg = 0, neu = 0;
    // Optimized loop for massive arrays
    for(let i=0; i<data.length; i++) {
        if(data[i].Sentiment === 'Positive') pos++;
        else if(data[i].Sentiment === 'Negative') neg++;
        else neu++;
    }
    document.getElementById("metric-total").textContent = data.length;
    document.getElementById("metric-positive").textContent = pos;
    document.getElementById("metric-negative").textContent = neg;
    document.getElementById("metric-neutral").textContent = neu;
}

// ---------------- TABLE ----------------
function renderTable(data){
    const tbody = document.getElementById('resultsTableBody');
    if(!data.length){
        tbody.innerHTML=`<tr><td colspan="5" class="p-4 text-center">No Data</td></tr>`; 
        return;
    }

    // 🔥 SPEED HACK: Use an array and .join() instead of innerHTML += 
    // 🔥 UX HACK: Limit to 500 rows to prevent browser freezing
    const limit = Math.min(data.length, 500);
    const htmlArray = [];

    for(let i=0; i < limit; i++){
        const r = data[i];
        const cls = r.Sentiment==='Positive'?'text-green-600 font-bold':r.Sentiment==='Negative'?'text-red-600 font-bold':'text-yellow-600 font-bold';
        
        // 5 COLUMNS TO MATCH HTML
        htmlArray.push(`<tr>
            <td class="px-4 py-2 border-b">${r.Text}</td>
            <td class="px-4 py-2 border-b text-center text-green-600 font-bold">+${r.Positive || 0}</td>
            <td class="px-4 py-2 border-b text-center text-red-600 font-bold">-${r.Negative || 0}</td>
            <td class="px-4 py-2 border-b text-center font-bold">${r.Score}</td>
            <td class="px-4 py-2 border-b text-center ${cls}">${r.Sentiment}</td>
        </tr>`);
    }

    if(data.length > 500) {
        htmlArray.push(`<tr><td colspan="5" class="p-4 text-center text-gray-500 font-bold bg-gray-50">Showing top 500 of ${data.length} records to keep your browser fast. Export CSV to see all.</td></tr>`);
    }

    tbody.innerHTML = htmlArray.join('');
}

// ---------------- CHARTS ----------------
function destroyCharts(){
    if(sentimentChart) sentimentChart.destroy();
    if(scoreBarChart) scoreBarChart.destroy();
    if(topWordsChart) topWordsChart.destroy();
}

function renderCharts(data){
    destroyCharts();
    let pos = 0, neg = 0, neu = 0;
    const counts = {};

    // Single pass loop to gather all chart data extremely fast
    for(let i=0; i<data.length; i++) {
        const r = data[i];
        if(r.Sentiment === 'Positive') pos++;
        else if(r.Sentiment === 'Negative') neg++;
        else neu++;
        counts[r.Score] = (counts[r.Score]||0)+1;
    }

    sentimentChart = new Chart(document.getElementById('sentimentChart'),{
        type:'doughnut',
        data:{
            labels:['Positive','Negative','Neutral'], 
            datasets:[{label:'Sentiment', data:[pos,neg,neu], backgroundColor:['#16a34a','#dc2626','#eab308']}]
        },
        options: { plugins: { legend: { position: 'bottom' } } }
    });
    
    // Sort bar chart sequentially
    const sortedScores = Object.keys(counts).sort((a,b) => a-b);
    const sortedCounts = sortedScores.map(score => counts[score]);

    scoreBarChart = new Chart(document.getElementById('scoreBarChart'),{
        type:'bar',
        data:{
            labels:sortedScores, 
            datasets:[{label:'Number of Reviews', data:sortedCounts, backgroundColor:'#7c3aed', borderRadius: 4}]
        },
        options: { plugins: { legend: { display: false } } }
    });
}

// ---------------- TOP WORDS ----------------
function renderTopWordsChart(data){
    const wordCounts = {};
    // Use a Set for lightning-fast lookups
    const stopWords = new Set(["the","is","and","to","a","of","in","it","for","on","this","that","not","too","very","with","are","was","be"]);

    // Limit scanning to a sample of 10,000 max to save CPU processing time
    const limit = Math.min(data.length, 10000);

    for(let i=0; i<limit; i++) {
        const words = data[i].Text.toLowerCase().match(/\b[a-z]{3,}\b/g); // Match words > 2 letters
        if(words) {
            for(let j=0; j<words.length; j++){
                const w = words[j];
                if(!stopWords.has(w)) {
                    wordCounts[w] = (wordCounts[w]||0)+1;
                }
            }
        }
    }

    const top = Object.entries(wordCounts).sort((a,b)=>b[1]-a[1]).slice(0,10);
    topWordsChart = new Chart(document.getElementById('topWordsChart'),{
        type:'bar',
        data:{
            labels:top.map(x=>x[0]), 
            datasets:[{label:'Word Count', data:top.map(x=>x[1]), backgroundColor:'#f97316', borderRadius: 4}]
        },
        options:{
            indexAxis:'y', 
            responsive:true,
            plugins: { legend: { display: false } }
        }
    });
}

// ---------------- EXPORT ----------------

// Button 1: Download ONLY the filtered/searched data
exportFilteredBtn.addEventListener('click', () => {
    if(!filteredData || filteredData.length === 0){
        alert("No filtered data to export!"); 
        return;
    }
    
    const originalText = exportFilteredBtn.textContent;
    exportFilteredBtn.textContent = "Generating...";
    exportFilteredBtn.disabled = true;

    setTimeout(() => {
        exportCSV(filteredData, 'Filtered_Customer_Reviews.csv');
        exportFilteredBtn.textContent = originalText;
        exportFilteredBtn.disabled = false;
    }, 100);
});

// Button 2: Download ALL data (e.g., all 50,000 records)
exportFullBtn.addEventListener('click', () => {
    if(!currentData || currentData.length === 0){
        alert("No data to export!"); 
        return;
    }
    
    const originalText = exportFullBtn.textContent;
    exportFullBtn.textContent = "Generating...";
    exportFullBtn.disabled = true;

    setTimeout(() => {
        exportCSV(currentData, 'All_Customer_Reviews.csv');
        exportFullBtn.textContent = originalText;
        exportFullBtn.disabled = false;
    }, 100);
});

// The core CSV generator function
function exportCSV(data, filename) {
    // 🔥 Updated headers to exactly match your beautiful dashboard table!
    const csv = ['Review Output,Pos Words,Neg Words,Total Score,Classification']; 
    
    for (let i = 0; i < data.length; i++) {
        // Safely escape quotes inside the review text so Excel doesn't break
        let safeText = data[i].Text.replace(/"/g, '""'); 
        csv.push(`"${safeText}",${data[i].Positive || 0},${data[i].Negative || 0},${data[i].Score},${data[i].Sentiment}`);
    }
    
    // Create the downloadable file
    const blob = new Blob([csv.join('\n')], { type: 'text/csv;charset=utf-8;' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = filename;
    
    // Trigger the download automatically
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}