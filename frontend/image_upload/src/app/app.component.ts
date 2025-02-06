import { Component } from '@angular/core';
import { UploadFormComponent } from './components/upload-form/upload-form.component';

@Component({
  selector: 'app-root',
  imports: [UploadFormComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title: string = 'Image Upload';
}
