/**
 * Drawing API for managing canvas elements.
 * This provides the interface that the MCP server will use.
 */

interface Circle {
    id: string;
    x: number;
    y: number;
    radius: number;
    color: string;
}

interface Rectangle {
    id: string;
    x: number;
    y: number;
    width: number;
    height: number;
    color: string;
}

type Element = Circle | Rectangle;

export class DrawingAPI {
    private elements: Map<string, Element> = new Map();

    drawCircle(data: Circle): Circle {
        this.elements.set(data.id, data);
        return data;
    }

    drawRectangle(data: Rectangle): Rectangle {
        this.elements.set(data.id, data);
        return data;
    }

    getElements(): Element[] {
        return Array.from(this.elements.values());
    }

    getElementById(id: string): Element | undefined {
        return this.elements.get(id);
    }

    deleteElement(id: string): boolean {
        return this.elements.delete(id);
    }

    clearCanvas(): void {
        this.elements.clear();
    }

    loadElements(elements: Element[]): void {
        this.elements.clear();
        elements.forEach(element => {
            this.elements.set(element.id, element);
        });
    }
}
