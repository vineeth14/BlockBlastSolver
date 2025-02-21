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
  @Input() completionCounter: any | null = null;
  readonly boardSize = [0, 1, 2, 3, 4, 5, 6, 7]; // 8x8 grid indices

  ngOnInit(): void {
    console.log(this.completionCounter);
  }
  getColorForCell(value: number): string {
    switch(value) {
      case 1: return '#cdb4db'; // Purple
      case 2: return '#90a955'; // Green
      case 3: return '#e76f51'; // Orange
      case 4: return '#e9c46a'; // Yellow
      default: return '#edede9'; // White
    }
  }
}
