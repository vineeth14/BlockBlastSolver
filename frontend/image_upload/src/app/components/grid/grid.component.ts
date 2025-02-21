import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-grid',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './grid.component.html',
  styleUrl: './grid.component.css'
})
export class GridComponent {
  @Input() gridData: any[][] | null = null;
  readonly boardSize = [0, 1, 2, 3, 4, 5, 6, 7]; // 8x8 grid indices

  getColorForCell(value: number): string {
    switch(value) {
      case 1: return '#4CAF50'; // Green
      case 2: return '#2196F3'; // Blue
      case 3: return '#F44336'; // Red
      case 4: return '#FFEB3B'; // Yellow
      default: return '#FFFFFF'; // White
    }
  }
}
