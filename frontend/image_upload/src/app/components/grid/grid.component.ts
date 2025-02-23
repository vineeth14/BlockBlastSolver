import { Component, Input, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-grid',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './grid.component.html',
  styleUrl: './grid.component.css'
})
export class GridComponent implements OnInit {
  @Input() grid: number[][] | null = null;
  @Input() title: string = '';
  @Input() completedRows: number | null = null;
  @Input() completedColumns: number | null = null;

  rowIndices: number[] = [];
  columnIndices: number[] = [];

  ngOnInit(): void {
    if (this.grid && this.grid.length > 0) {
      // Get number of rows
      const numRows = this.grid.length;
      this.rowIndices = [];
      for (let i = 0; i < numRows; i++) {
        this.rowIndices.push(i);
      }
      
      const numCols = this.grid[0]?.length || 0;
      this.columnIndices = [];
      for (let i = 0; i < numCols; i++) {
        this.columnIndices.push(i);
      }
    }
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
