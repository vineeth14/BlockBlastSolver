import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { GridComponent } from '../grid/grid.component';

@Component({
  selector: 'app-upload-form',
  standalone: true,
  imports: [CommonModule, HttpClientModule, GridComponent],
  templateUrl: './upload-form.component.html',
  styleUrl: './upload-form.component.css'
})
export class UploadFormComponent {
  outputBoxVisible = false;
  progress = `0%`;
  uploadResult = '';
  fileName = '';
  fileSize = '';
  uploadStatus: number | undefined;
  gridData: any[][] | null = null;
  private apiUrl = 'http://localhost:8000/upload/'

  constructor(private http: HttpClient) {}

  onFileSelected(event: any, inputFile: File | null) {
    this.outputBoxVisible = false;
    this.progress = `0%`;
    this.uploadResult = '';
    this.fileName = '';
    this.fileSize = '';
    this.uploadStatus = undefined;
    const file: File = inputFile || event.target.files[0];

    if (file) {
      this.fileName = file.name;
      this.fileSize = `${(file.size / 1024).toFixed(2)} KB`;
      this.outputBoxVisible = true;

      const formData = new FormData();
      formData.append('file', file);

      this.http.post(this.apiUrl, formData)
      .subscribe({
        next: (response: any) => {
          this.uploadResult = 'Uploaded';
          this.uploadStatus = 200;
          this.gridData = response[1];
          
        },
        error: (error: any) => {
          if (error.status === 400) {
            this.uploadResult = error.error.message;
          } else{
            this.uploadResult = 'File upload failed!';
          }
          this.uploadStatus = error.status;
        }
      });
    }
  }

  handleDragOver(event: DragEvent) {
    event.preventDefault();
    event.stopPropagation();
  }

  handleDrop(event: DragEvent) {
    event.preventDefault();
    if (event.dataTransfer) {
      const file: File = event.dataTransfer.files[0];
      this.onFileSelected(event, event.dataTransfer.files[0]);
    }
  }

  
}
