import React, { useEffect } from "react";
import lottie from "lottie-web";
import animationData from "./Animation - 1724592154152.json";
import "./Loading.css"

function Loading() {
  useEffect(() => {
    const animationContainer = document.getElementById("animation-container");
    if (animationContainer) {
      const anim = lottie.loadAnimation({
        container: animationContainer,
        renderer: "svg",
        loop: true,
        autoplay: true,
        animationData: animationData,
      });

      // Clean up animation when component unmounts
      return () => {
        anim.destroy();
      };
    }
  }, []); // Run only once when the component mounts

  return (
    <div className="loading">
      <div
        id="animation-container"
        style={{ width: "50%", height: "50%" }}
      ></div>
    </div>
  );
}

export default Loading;
