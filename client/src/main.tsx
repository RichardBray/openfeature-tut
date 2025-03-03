import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import App from "./App.tsx";
import { OpenFeatureProvider, OpenFeature } from "@openfeature/react-sdk";
import { FlagdWebProvider } from "@openfeature/flagd-web-provider";

OpenFeature.setProvider(
  new FlagdWebProvider({
    host: "localhost",
    port: 8013,
    tls: false,
  }),
  {
    deviceType: window.innerWidth <= 768 ? "mobile" : "desktop",
  }
);

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <OpenFeatureProvider>
      <App />
    </OpenFeatureProvider>
  </StrictMode>
);
