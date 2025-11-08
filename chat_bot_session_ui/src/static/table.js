 // Data for Tests table
    const ROWS = [
        {
            "User Query": "What is the capital of France?",
            "Ground Truth": "Paris",
            "Generated Output": "Paris",
            "Relevance": {label: "Very Relevant", badge: "relevant", emoji: "✅"}
        },
        {
            "User Query": "Summarize the theory of evolution.",
            "Ground Truth": "Evolution describes the process by which species change over time through natural selection.",
            "Generated Output": "Species adapt and change gradually over generations due to natural selection.",
            "Relevance": {label: "Very Relevant", badge: "relevant", emoji: "✅"}
        },
        {
            "User Query": "Translate \"Hello\" to Spanish.",
            "Ground Truth": "Hola",
            "Generated Output": "Hola",
            "Relevance": {label: "Very Relevant", badge: "relevant", emoji: "✅"}
        },
        {
            "User Query": "Who wrote '1984'?",
            "Ground Truth": "George Orwell",
            "Generated Output": "George Orwell",
            "Relevance": {label: "Very Relevant", badge: "relevant", emoji: "✅"}
        },
        {
            "User Query": "Explain Python list comprehensions.",
            "Ground Truth": "List comprehensions provide a concise way to create lists using a single line of code.",
            "Generated Output": "A Python list comprehension is a compact way to create lists from iterables.",
            "Relevance": {label: "Quite Relevant", badge: "quite", emoji: "✅"}
        },
        {
            "User Query": "What is the boiling point of water?",
            "Ground Truth": "100°C at standard atmospheric pressure.",
            "Generated Output": "100 degrees Celsius.",
            "Relevance": {label: "Quite Relevant", badge: "quite", emoji: "✔️"}
        },
        {
            "User Query": "Name a city in Germany.",
            "Ground Truth": "Berlin",
            "Generated Output": "Munich",
            "Relevance": {label: "Less Relevant", badge: "less", emoji: "🟡"}
        },
        {
            "User Query": "What is photosynthesis?",
            "Ground Truth": "It is the process by which green plants convert sunlight, water, and CO2 into glucose and oxygen.",
            "Generated Output": "Plants need sunlight to live.",
            "Relevance": {label: "Less Relevant", badge: "less", emoji: "🟡"}
        },
        {
            "User Query": "What is 2 + 2?",
            "Ground Truth": "4",
            "Generated Output": "5",
            "Relevance": {label: "Bad Relevance", badge: "bad", emoji: "❌"}
        },
        {
            "User Query": "Define gravity.",
            "Ground Truth": "A natural force causing objects to be attracted toward the center of the Earth or other physical bodies.",
            "Generated Output": "It is related to levitation.",
            "Relevance": {label: "Bad Relevance", badge: "bad", emoji: "❌"}
        }
    ];

    // Tests Table Columns
    const COLUMNS = [
        { key: "User Query", label: "User Query", className: "user-query-cell", widthWeight: 1 },
        { key: "Ground Truth", label: "Ground Truth", widthWeight: 2 },
        { key: "Generated Output", label: "Generated Output", widthWeight: 1 },
        { key: "Relevance", label: "Relevance", widthWeight: 1 }
    ];

    function setColumnWidths(table, columns) {
        // Add a new column for Run at the end for layout, but with minimal weight.
        const allCols = [...columns, { key: "__run_btn__", label: "", widthWeight: 0.4 }];
        const totalWeight = allCols.reduce((s, col) => s + (col.widthWeight || 1), 0);
        let colgroup = table.querySelector('colgroup');
        if (colgroup) colgroup.remove();
        colgroup = document.createElement('colgroup');
        allCols.forEach((col, idx) => {
            const colEl = document.createElement('col');
            colEl.className = 'col-' + (idx+1);
            const perc = ((col.widthWeight||1) / totalWeight * 100).toFixed(3);
            colEl.style.width = perc+'%';
            colgroup.appendChild(colEl);
        });
        table.insertBefore(colgroup, table.firstChild);
    }

    function renderTable( columns, dataRows,table_name="") {

        let tables_container = document.getElementById("interactive-table-container") ; 


        // We'll always append the Run button column as the last column
        const tableTitle = document.createElement("div");
        tableTitle.className = "table-title";

        // Create inner span container  
        const innerSpan = document.createElement("span");
        innerSpan.style.display = "flex";
        innerSpan.style.alignItems = "center";
        innerSpan.style.gap = "0.45em";

        // Create emoji span
        const emojiSpan = document.createElement("span");
        emojiSpan.className = "table-title-emoji";
        emojiSpan.textContent = "📝";

        // Append emoji and text to inner span
        innerSpan.appendChild(emojiSpan);
        innerSpan.append(table_name);

        // Create button
        const button = document.createElement("button");
        button.className = "run-test-btn";
        button.id = "run-test-btn";
        button.type = "button";
        button.textContent = "Run";

        // Append everything to main div
        tableTitle.appendChild(innerSpan);
        tableTitle.appendChild(button);

        tables_container.prepend(tableTitle)

        let table = document.createElement("table");
        table.className = "interactive-table";
        table.cellSpacing = "0";
        table.id = "main-table";

        // Create thead
        let thead = document.createElement("thead");
        
        let tbody = document.createElement("tbody");

        // Append thead and tbody to the table
        table.appendChild(thead);
        table.appendChild(tbody);


        if (tables_container.children.length >= 1) {
  tables_container.insertBefore(table, tables_container.children[1]);
} else {
  tables_container.appendChild(table);
}

        // tables_container.append(table) ; 



        setColumnWidths(table, columns);

        // Header
         thead = table.querySelector('thead');
        thead.innerHTML = '';
        const trHead = document.createElement('tr');
        columns.forEach((col, idx) => {
            const th = document.createElement('th');
            th.textContent = col.label;
            th.classList.add('col-' + (idx+1));
            trHead.appendChild(th);
        });
        // --- Run column th ---
        const thRun = document.createElement('th');
        thRun.textContent = 'Run';  // or use an icon: '▶' or '⏵'
        thRun.classList.add('col-' + (columns.length+1));
        trHead.appendChild(thRun);

        thead.appendChild(trHead);

        // Body
         tbody = table.querySelector('tbody');
        tbody.innerHTML = '';
        dataRows.forEach((row, rowIdx) => {
            const tr = document.createElement('tr');
            columns.forEach((col, idx) => {
                const td = document.createElement('td');
                td.classList.add('col-' + (idx+1));
                if (col.key === "User Query") {
                    td.classList.add('user-query-cell');
                }
                if (col.key !== "Relevance") {
                    td.textContent = row[col.key];
                } else {
                    // Badge
                    const span = document.createElement('span');
                    span.className = `rel-badge ${row.Relevance.badge}`;
                    const checkEmoji = document.createElement('span');
                    checkEmoji.className = 'check-emoji';
                    checkEmoji.textContent = row.Relevance.emoji;
                    span.appendChild(checkEmoji);
                    span.appendChild(document.createTextNode(' ' + row.Relevance.label));
                    td.appendChild(span);
                }
                tr.appendChild(td);
            });
            // --- Row Run Button cell ---
            const tdRun = document.createElement('td');
            tdRun.classList.add('col-' + (columns.length+1));
            tdRun.style.textAlign = "center";
            tdRun.style.verticalAlign = "middle";
            tdRun.style.cursor = "default";
            // Run Button in row:
            const btn = document.createElement('button');
            btn.type = "button";
            btn.className = "row-run-btn";
            btn.setAttribute('aria-label', 'Run this test');
            btn.innerHTML = 'Run';
            btn.onclick = function(e){

                e.stopPropagation();
                let test_2_run = {
                  user_query: row["User Query"],
                  row_num: rowIdx  
                }
                fetch ("http://localhost:3030/run_tests" , {
                    method : 'POST' , 
                    headers : {
                        'Content-Type': 'application/json' , 
                    }, 
                    body : JSON.stringify({
                        "tests" : [test_2_run],
                    })
                }).then(response => response.json())
                .then(result => console.log(result))
                .catch(error => console.error('Error:', error));
                // Print only user_query and row_num per requirements
                console.log({
                  user_query: row["User Query"],
                  row_num: rowIdx
                });
            };
            tdRun.appendChild(btn);
            tr.appendChild(tdRun);

            tbody.appendChild(tr);
        });



    }

    // Initial State: Tests selected, show table
    renderTable( COLUMNS, ROWS,"Test soviet");
    // renderTable( COLUMNS, ROWS,"Test 2");
  
    // --- Add Test Set Button logic ---
    // -- BEGIN PATCH: Form reset logic --
    function resetAddTestSetFormToInitial() {
        // Reset the form fields to the initial state
        var f = document.getElementById('add-test-set-form');
        if (f) {
            f.reset();
        }
        // Uncheck and check the checkboxes as per initial (checked for both)
        var userQCb = document.querySelector('#add-ts-columns input[type="checkbox"][value="User Query"]');
        var gtCb = document.querySelector('#add-ts-columns input[type="checkbox"][value="Ground Truth"]');
        if (userQCb) userQCb.checked = true;
        if (gtCb) gtCb.checked = true;
        // Reset Metrics dropdown to first option (disabled)
        var metricsSel = document.getElementById("add-test-set-form-metrics-select");
        if (metricsSel) metricsSel.selectedIndex = 0;
        // Clear and hide ai-judge custom fields
        var aiFields = document.getElementById('ai-as-judge-fields-container');
        if (aiFields) aiFields.innerHTML = '';
        if (aiFields) aiFields.style.display = 'none';
    }

    window.AddTestSet = function() {
        // Reset the form to initial state every time before showing
        resetAddTestSetFormToInitial();
        // Show the add test set form
        var formWrap = document.getElementById('add-test-set-form-wrap');
        if (!formWrap.classList.contains('active')) {
            formWrap.classList.add('active');
        }
    };
    // -- END PATCH: Form reset logic --

    var addTestSetBtn = document.getElementById('add-test-set-btn');
    if (addTestSetBtn) {
        addTestSetBtn.onclick = function() {
            window.AddTestSet();
        }
    }

    // Add Test Set Cancel button logic
    var addTestSetCancelBtn = document.getElementById('add-test-set-cancel-btn');
    if (addTestSetCancelBtn) {
        addTestSetCancelBtn.onclick = function() {
            var formWrap = document.getElementById('add-test-set-form-wrap');
            formWrap.classList.remove('active');
            // Also clear ai-judge fields when closing
            const aiFields = document.getElementById('ai-as-judge-fields-container');
            if (aiFields) aiFields.innerHTML = '';
            if (aiFields) aiFields.style.display = 'none';
            // PATCH: Also reset the form to clear fields
            resetAddTestSetFormToInitial();
        }
    }
    // Add Test Set Build button: minimal change to implement requirement
    var addTestSetBuildBtn = document.getElementById('add-test-set-build-btn');
    if (addTestSetBuildBtn) {
        addTestSetBuildBtn.onclick = function() {
            // Collect checked columns
            var colInputs = document.querySelectorAll('#add-ts-columns input[type="checkbox"]:checked');
            var cols = [];
            colInputs.forEach(function(input){ cols.push(input.value); });

            // Collect AI as judge fields
            var ai_oj = [];
            var aiJudgeLists = document.querySelectorAll('.ai-judge-display-list');
            // If exists (there could be one .ai-judge-display-list per metrics block, but only one here)
            if (aiJudgeLists.length) {
                aiJudgeLists.forEach(function(displayList){
                    var judges = displayList.querySelectorAll('.ai-judge-collapsible-toggle');
                    judges.forEach(function(judgeBtn){
                        // Name: get strong + span text
                        var nameSpan = judgeBtn.querySelector('span:last-child');
                        var name = "";
                        if (nameSpan) {
                            // Try to get just the colored part
                            var inHtml = nameSpan.innerHTML.match(/<span[^>]*>(.*?)<\/span>/);
                            name = inHtml ? inHtml[1].trim() : nameSpan.textContent.replace(/^Name:\s*/i,'').trim();
                        }
                        // Prompt: look at next sibling (collapsible div)
                        var prompt = "";
                        var wrapper = judgeBtn.parentNode;
                        var promptDiv = wrapper.querySelector('.ai-judge-collapsible-content');
                        if (promptDiv) {
                            // Pre is inside, just get its text
                            var pre = promptDiv.querySelector('pre');
                            if (pre) prompt = pre.textContent.trim();
                        }
                        ai_oj.push({name: name, prompt: prompt});
                    });
                });
            }

            var resultObj = {
                Cols: cols,
                metrics: {
                    AI_as_a_judge: ai_oj
                }
            };
            let zebi = []
        renderTable( COLUMNS, zebi,"Test soviet");

            console.log("oué mon gaté")
            console.log(resultObj);
            

            // Hide form as before
            var formWrap = document.getElementById('add-test-set-form-wrap');
            formWrap.classList.remove('active');
            // Also clear ai-judge fields when hiding
            const aiFields = document.getElementById('ai-as-judge-fields-container');
            if (aiFields) aiFields.innerHTML = '';
            if (aiFields) aiFields.style.display = 'none';
            // PATCH: Also reset the form fields when building
            resetAddTestSetFormToInitial();
        }
    }

    // --- Upload Test Set Input logic ---
    window.UploadTestSet = function(files) {
        // handle FileList or single File
        if (files && files.length > 0) {
            console.log('User selected files for upload:');
            for (let i = 0; i < files.length; i++) {
                console.log(`File ${i + 1}:`, files[i].name);
            }
        }
    };

    // Hide previous button logic, use input instead
    var uploadTestSetInput = document.getElementById('upload-test-set-input');
    if (uploadTestSetInput) {
        uploadTestSetInput.addEventListener('change', function(e) {
            window.UploadTestSet(uploadTestSetInput.files);
            // Optionally, reset after upload
            uploadTestSetInput.value = '';
        });
    }

    // ----------- LOGIC FOR AI AS JUDGE FIELDS IN FORM ---------------
    var aiFieldsContainer = document.getElementById("ai-as-judge-fields-container");
    var metricsSelect = document.getElementById("add-test-set-form-metrics-select");

    function createAiJudgeFields() {
        // Avoid duplicate
        if (!aiFieldsContainer) return;
        aiFieldsContainer.innerHTML = `
            <div class="add-ai-judge-fields" id="add-ai-judge-fields-main">
              <div>
                <label for="ai-judge-name">Name</label>
                <input type="text" id="ai-judge-name" name="ai_judge_name" placeholder="e.g. Custom Judge Name" autocomplete="off">
              </div>
              <div>
                <label for="ai-judge-prompt">Prompt</label>
                <textarea id="ai-judge-prompt" name="ai_judge_prompt" placeholder="Prompt for AI as judge..." rows="4"></textarea>
              </div>
              <button type="button" class="add-ai-judge-btn" id="add-ai-judge-btn">Add</button>
            </div>
        `;
        aiFieldsContainer.style.display = '';

        // Basic logic for the add button (prevent default submit), can extend as needed
        setTimeout(function() {
            var addBtn = document.getElementById("add-ai-judge-btn");
            if (addBtn) {
                addBtn.onclick = function(e) {
                    e.preventDefault();
                    var nameValue = document.getElementById("ai-judge-name").value.trim();
                    var promptValue = document.getElementById("ai-judge-prompt").value.trim();
                    if (!nameValue || !promptValue) {
                        addBtn.textContent = "Please provide Name & Prompt";
                        addBtn.style.background = "linear-gradient(90deg,#ffbbaa 65%,#ff7474 100%)";
                        setTimeout(function() {
                            addBtn.textContent = "Add";
                            addBtn.style.background = "";
                        }, 1100);
                        return;
                    }
                    // Success
                    addBtn.textContent = "Added!";
                    addBtn.style.background = "linear-gradient(90deg,#41d89d 70%,#9bf7a7 100%)";
                    // Log the given name and prompt
                    console.log("AI Judge Name:", nameValue);
                    console.log("AI Judge Prompt:", promptValue);

                    // Create the collapsible divs
                    var wrapperDiv = document.createElement("div");
                    wrapperDiv.className = "ai-judge-collapsible";
                    wrapperDiv.style.margin = "1em 0 0.4em 0";
                    wrapperDiv.style.borderRadius = "0.42em";
                    wrapperDiv.style.background = "#f5fafc";
                    wrapperDiv.style.boxShadow = "0 1.5px 9px #cbe5fb1f";
                    wrapperDiv.style.padding = "0";

                    // Button/header to show Name, acts as the toggle
                    var toggleBtn = document.createElement("button");
                    toggleBtn.type = "button";
                    toggleBtn.className = "ai-judge-collapsible-toggle";
                    toggleBtn.style.width = "100%";
                    toggleBtn.style.background = "none";
                    toggleBtn.style.border = "none";
                    toggleBtn.style.textAlign = "left";
                    toggleBtn.style.fontSize = "1.04em";
                    toggleBtn.style.fontWeight = "600";
                    toggleBtn.style.color = "#315699";
                    toggleBtn.style.cursor = "pointer";
                    toggleBtn.style.padding = "1em 0.9em";
                    toggleBtn.style.display = "flex";
                    toggleBtn.style.alignItems = "center";
                    // Caret icon for show/hide
                    var caret = document.createElement("span");
                    caret.className = "caret-collapsible-icon";
                    caret.textContent = "▶";
                    caret.style.marginRight = "0.6em";
                    caret.style.transition = "transform 0.16s";
                    toggleBtn.appendChild(caret);

                    var nameLabel = document.createElement("span");
                    nameLabel.innerHTML = "<strong>Name:</strong> " +
                        "<span style='color:#315699; font-weight:600'>" + nameValue + "</span>";
                    toggleBtn.appendChild(nameLabel);

                    // Collapsible panel for prompt
                    var collapsibleDiv = document.createElement("div");
                    collapsibleDiv.className = "ai-judge-collapsible-content";
                    collapsibleDiv.style.display = "none";
                    collapsibleDiv.style.padding = "0 0.9em 1.0em 2.7em";

                    collapsibleDiv.innerHTML = 
                        "<strong style='color:#24527b;'>Prompt:</strong><br>" +
                        "<pre style='background:none; display:block; color:#24527b; font-family:inherit; white-space:pre-wrap; margin:0;'>" + promptValue + "</pre>";

                    // Toggle event for collapsing/expanding
                    toggleBtn.onclick = function() {
                        var isOpen = collapsibleDiv.style.display === "block";
                        if (isOpen) {
                            collapsibleDiv.style.display = "none";
                            caret.style.transform = "";
                            caret.textContent = "▶";
                        } else {
                            collapsibleDiv.style.display = "block";
                            caret.style.transform = "rotate(90deg)";
                            caret.textContent = "▼";
                        }
                    };

                    wrapperDiv.appendChild(toggleBtn);
                    wrapperDiv.appendChild(collapsibleDiv);

                    // Insert into display container as before
                    var fieldsMain = document.getElementById("add-ai-judge-fields-main");
                    if (fieldsMain && fieldsMain.parentNode) {
                        var displayContainer = fieldsMain.parentNode.querySelector(".ai-judge-display-list");
                        if (!displayContainer) {
                            displayContainer = document.createElement("div");
                            displayContainer.className = "ai-judge-display-list";
                            displayContainer.style.marginTop = "1em";
                            fieldsMain.parentNode.insertBefore(displayContainer, fieldsMain.nextSibling);
                        }
                        displayContainer.appendChild(wrapperDiv);
                    }

                    setTimeout(function() {
                        addBtn.textContent = "Add";
                        addBtn.style.background = "";
                        document.getElementById("ai-judge-name").value = "";
                        document.getElementById("ai-judge-prompt").value = "";
                    }, 900);
                };
            }
        }, 8);
    }

    function hideAiJudgeFields() {
        if (!aiFieldsContainer) return;
        aiFieldsContainer.innerHTML = "";
        aiFieldsContainer.style.display = "none";
    }

    if (metricsSelect) {
        metricsSelect.addEventListener("change", function(e) {
            if (metricsSelect.value === "ai_as_judge") {
                createAiJudgeFields();
            } else {
                hideAiJudgeFields();
            }
        });
    }

    // Defensive: if form gets closed, also clear the AI judge fields
    var addTestSetForm = document.getElementById('add-test-set-form');
    addTestSetForm && addTestSetForm.addEventListener('reset', function() {
        hideAiJudgeFields();
    });

    // Minimal Run button handling (now prints list of dicts as required)
    var runTestBtn = document.getElementById('run-test-btn');
    if (runTestBtn) {
        runTestBtn.onclick = function() {
            // Compose an array with user_query and row_num for each row and log it
            const runList = ROWS.map((row, idx) => ({
                user_query: row["User Query"],
                row_num: idx
            }));
            fetch ("http://localhost:3030/run_tests" , {
                    method : 'POST' , 
                    headers : {
                        'Content-Type': 'application/json' , 
                    }, 
                    body : JSON.stringify({
                        "tests" : runList,
                    })
                }).then(response => response.json())
                .then(result => console.log(result))
                .catch(error => console.error('Error:', error));
            console.log(runList);
        };