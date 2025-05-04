from flask import Flask, render_template, request

app = Flask(__name__)

# FIFO Page Replacement Algorithm
def fifo(page_references, frames):
    page_faults = 0
    memory = []
    steps = []
    page_faults_list = []  # To store cumulative page fault count or "-"
    for page in page_references:
        if page not in memory:
            page_faults += 1
            page_faults_list.append(page_faults)  # Increment page fault count
            if len(memory) < frames:
                memory.append(page)
            else:
                memory.pop(0)
                memory.append(page)
        else:
            page_faults_list.append("-")  # No page fault
        steps.append(memory + ['_'] * (frames - len(memory)))
    return page_faults, steps, page_faults_list

# LRU Page Replacement Algorithm
def lru(page_references, frames):
    page_faults = 0
    memory = []
    recent_usage = {}
    steps = []
    page_faults_list = []  # To store cumulative page fault count or "-"
    for i, page in enumerate(page_references):
        if page not in memory:
            page_faults += 1
            page_faults_list.append(page_faults)  # Increment page fault count
            if len(memory) < frames:
                memory.append(page)
            else:
                # Find the least recently used page
                lru_page = min(recent_usage, key=recent_usage.get)
                if lru_page in memory:
                    memory.remove(lru_page)
                memory.append(page)
        else:
            page_faults_list.append("-")  # No page fault
        recent_usage[page] = i
        steps.append(memory + ['_'] * (frames - len(memory)))
    return page_faults, steps, page_faults_list

# Optimal Page Replacement Algorithm
def optimal(page_references, frames):
    page_faults = 0
    memory = []
    steps = []
    page_faults_list = []  # To store cumulative page fault count or "-"
    for i, page in enumerate(page_references):
        if page not in memory:
            page_faults += 1
            page_faults_list.append(page_faults)  # Increment page fault count
            if len(memory) < frames:
                memory.append(page)
            else:
                # Find the page that won't be used for the longest time
                future_use = {pg: (page_references[i + 1:].index(pg) if pg in page_references[i + 1:] else float('inf')) for pg in memory}
                farthest_page = max(future_use, key=future_use.get)
                memory.remove(farthest_page)
                memory.append(page)
        else:
            page_faults_list.append("-")  # No page fault
        steps.append(memory + ['_'] * (frames - len(memory)))
    return page_faults, steps, page_faults_list

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get inputs from the form
        page_references = list(map(int, request.form["pages"].split()))
        frames = int(request.form["frames"])
        
        # Calculate page faults and steps for each algorithm
        fifo_faults, fifo_steps, fifo_page_faults = fifo(page_references, frames)
        lru_faults, lru_steps, lru_page_faults = lru(page_references, frames)
        optimal_faults, optimal_steps, optimal_page_faults = optimal(page_references, frames)
        
        # Determine the best algorithm (minimum page faults)
        methods = {
            "FIFO": fifo_faults,
            "LRU": lru_faults,
            "Optimal": optimal_faults,
        }
        best_method = min(methods, key=methods.get)

        # Render results
        return render_template(
            "index.html",
            results={
                "fifo": {"faults": fifo_faults, "steps": fifo_steps, "page_faults": fifo_page_faults},
                "lru": {"faults": lru_faults, "steps": lru_steps, "page_faults": lru_page_faults},
                "optimal": {"faults": optimal_faults, "steps": optimal_steps, "page_faults": optimal_page_faults}
            },
            best_method=best_method,
            methods=methods,
            page_references=page_references,
            frames=frames,
            enumerate=enumerate  # Pass enumerate explicitly to the template
        )
    return render_template("index.html", results=None, enumerate=enumerate)

if __name__ == "__main__":
    app.run(debug=True)
