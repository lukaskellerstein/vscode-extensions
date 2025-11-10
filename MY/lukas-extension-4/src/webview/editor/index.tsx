interface Circle {
  x: number;
  y: number;
  radius: number;
  color: string;
}

interface DocumentData {
  circles: Circle[];
}

declare const acquireVsCodeApi: any;
const vscode = acquireVsCodeApi();

class LukeEditor {
  private canvas: HTMLCanvasElement;
  private ctx: CanvasRenderingContext2D;
  private circles: Circle[] = [];

  constructor() {
    this.canvas = document.getElementById("canvas") as HTMLCanvasElement;
    this.ctx = this.canvas.getContext("2d")!;

    this.setupCanvas();
    this.setupEventListeners();
    this.setupMessageListener();
  }

  private setupCanvas(): void {
    const resize = () => {
      this.canvas.width = window.innerWidth;
      this.canvas.height = window.innerHeight;
      this.render();
    };

    window.addEventListener("resize", resize);
    resize();
  }

  private setupEventListeners(): void {
    this.canvas.addEventListener("click", (e) => {
      const rect = this.canvas.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;

      const circle: Circle = {
        x,
        y,
        radius: 30,
        color: this.getRandomColor(),
      };

      vscode.postMessage({
        type: "addCircle",
        circle,
      });
    });
  }

  private setupMessageListener(): void {
    window.addEventListener("message", (event) => {
      const message = event.data;

      switch (message.type) {
        case "update":
          this.circles = message.data.circles || [];
          this.render();
          this.updateCount();
          break;
        case "addCircleFromSidebar":
          // Circle will be added via the update message after document is saved
          vscode.postMessage({
            type: "addCircle",
            circle: message.circle,
          });
          break;
      }
    });
  }

  private render(): void {
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

    for (const circle of this.circles) {
      this.drawCircle(circle);
    }
  }

  private drawCircle(circle: Circle): void {
    this.ctx.beginPath();
    this.ctx.arc(circle.x, circle.y, circle.radius, 0, Math.PI * 2);
    this.ctx.fillStyle = circle.color;
    this.ctx.fill();
    this.ctx.strokeStyle = "#000";
    this.ctx.lineWidth = 2;
    this.ctx.stroke();
  }

  private getRandomColor(): string {
    const colors = [
      "#e74c3c",
      "#3498db",
      "#2ecc71",
      "#f39c12",
      "#9b59b6",
      "#1abc9c",
    ];
    return colors[Math.floor(Math.random() * colors.length)];
  }

  private updateCount(): void {
    const countElement = document.getElementById("count");
    if (countElement) {
      countElement.textContent = this.circles.length.toString();
    }
  }
}

new LukeEditor();
