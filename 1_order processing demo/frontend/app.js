const API = "http://localhost:8000";
const STEPS = ["Order Created", "Payment Processing", "Preparing Order", "Order Completed"];

const btn = document.getElementById("createBtn");
const stepsEl = document.getElementById("steps");
const orderIdEl = document.getElementById("orderId");
let errorEl = document.getElementById("error");
if (!errorEl) {
  errorEl = document.createElement("p");
  errorEl.id = "error";
  errorEl.style.color = "#b91c1c";
  orderIdEl.after(errorEl);
}

function showError(msg) {
  errorEl.textContent = msg;
  console.error(msg);
}

function render(current) {
  const finished = current === STEPS.length - 1;
  stepsEl.innerHTML = STEPS.map((s, i) => {
    let cls = "";
    if (i < current || finished) cls = "done";
    else if (i === current) cls = "active";
    return `<li class="${cls}">${s}</li>`;
  }).join("");
}

async function poll(orderId) {
  try {
    const res = await fetch(`${API}/orders/${orderId}`, { cache: "no-store" });
    if (!res.ok) throw new Error(`GET /orders/${orderId} returned ${res.status}`);
    const data = await res.json();
    errorEl.textContent = "";
    render(data.step);
    orderIdEl.textContent = `Order ID: ${orderId} - status: ${data.status}`;
    if (data.step === STEPS.length - 1) {
      btn.disabled = false;
      return;
    }
  } catch (err) {
    // The worker may not be ready yet; show the problem and keep retrying.
    showError(`${err.message} - retrying...`);
  }
  setTimeout(() => poll(orderId), 1000);
}

btn.addEventListener("click", async () => {
  btn.disabled = true;
  errorEl.textContent = "";
  try {
    const res = await fetch(`${API}/orders`, { method: "POST" });
    if (!res.ok) throw new Error(`POST /orders returned ${res.status}`);
    const { order_id } = await res.json();
    orderIdEl.textContent = `Order ID: ${order_id}`;
    render(0);
    poll(order_id);
  } catch (err) {
    showError(`Could not reach the API at ${API}: ${err.message}`);
    btn.disabled = false;
  }
});

render(-1);