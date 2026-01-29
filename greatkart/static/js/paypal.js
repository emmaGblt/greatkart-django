const paypalScript = document.getElementById("paypalScript");
const amount = paypalScript.getAttribute("data-amount");

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
      console.log("details", details);
      // Show a success message to the buyer
      alert("Transation completed by " + details.payer.name.given_name + "!");
    });
  },
});
paypalButtons.render("#paypal-button-container");
