window.onload = () => {
  const currentPath = window.location.pathname;
  const robotWrapper = document.querySelector('.robot-wrapper');
  const heroContainer = document.querySelector('.hero-container');

  if (currentPath.includes('/login') || currentPath.includes('/register')) {
    if (robotWrapper) robotWrapper.style.display = 'none';
    if (heroContainer) heroContainer.style.display = 'none';
    return;
  }

  const container = document.getElementById("bg-canvas");

  for (let i = 0; i < 50; i++) {
    const bubble = document.createElement("div");
    const particle = document.createElement("div");

    bubble.className = "bubble";
    particle.className = "particle";

    // Bubble
    bubble.style.width = bubble.style.height = Math.random() * 40 + 10 + "px";
    bubble.style.left = Math.random() * window.innerWidth + "px";
    bubble.style.top = Math.random() * window.innerHeight + "px";
    bubble.style.setProperty("--duration", Math.random() * 6 + 4 + "s");
    bubble.style.animationDelay = Math.random() * 10 + "s";

    // Particle
    particle.style.width = particle.style.height = Math.random() * 4 + 1 + "px";
    particle.style.left = Math.random() * window.innerWidth + "px";
    particle.style.top = Math.random() * window.innerHeight + "px";
    particle.style.setProperty("--duration", Math.random() * 8 + 6 + "s");
    particle.style.animationDelay = Math.random() * 10 + "s";

    container.appendChild(bubble);
    container.appendChild(particle);
  }
};
