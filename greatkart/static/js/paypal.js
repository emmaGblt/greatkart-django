// Get paypal script from Django template
const paypalScript = document.getElementById("paypalScript");

// Get script dataset
const scriptData = paypalScript?.dataset;

// Retrieve the data
const amount = scriptData?.amount;
const paymentsUrl = scriptData?.paymentsUrl;
const orderReference = scriptData?.orderReference;
const redirectUrl = scriptData?.redirectUrl;

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function savePaymentData(details) {
  fetch(paymentsUrl, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify({
      order_reference: orderReference,
      transaction_id: details.id,
      payment_method: "paypal",
      status: details.status,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      const { order_reference: orderReference, transaction_id: transactionId } =
        data;
      const searchParams = new URLSearchParams({
        order_reference: orderReference,
        transaction_id: transactionId,
      });
      window.location.href = `${redirectUrl}?${searchParams.toString()}`;
    });
}

const paypalButtons = window.paypal.Buttons({
  style: {
    shape: "rect",
    layout: "vertical",
    color: "blue",
    label: "paypal",
  },

  async createOrder(data, actions) {
    return actions.order.create({
      purchase_units: [{ amount: { value: amount } }],
    });
  },

  async onApprove(data, actions) {
    return actions.order.capture().then((details) => {
      savePaymentData(details);
    });
  },
});
paypalButtons.render("#paypal-button-container");
