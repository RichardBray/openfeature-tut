import "./App.css";
import { useState } from "react";

function App() {
  const [apiMessage, setApiMessage] = useState<string>("");

  async function handleBuyNow() {
    try {
      const response = await fetch("http://localhost:3001/api/buy-now");
      const data = await response.json();
      setApiMessage(data.message);
    } catch (error) {
      setApiMessage("Error processing purchase. Please try again.");
    }
  }

  return (
    <>
      <h1>My Cool Store</h1>
      <div className="card">
        <h2>My cool item</h2>
        <p>This is the best item ever</p>
        <button type="button" onClick={handleBuyNow}>
          Buy Now
        </button>
        {apiMessage && (
          <p role="status" aria-live="polite">
            {apiMessage}
          </p>
        )}
      </div>
    </>
  );
}

export default App;
