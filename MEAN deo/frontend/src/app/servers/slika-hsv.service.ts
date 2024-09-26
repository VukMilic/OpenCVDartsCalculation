import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SlikaHsvService {
  private apiUrl = 'http://localhost:5000';  // Your Flask API URL

  constructor(private http: HttpClient) {}

  uploadImage(file: File): Observable<any> {
    const formData = new FormData();
    formData.append('file', file);
    return this.http.post(`${this.apiUrl}/upload`, formData);
  }

  getHSV(x: number, y: number, imagePath: string, removeImage: number): Observable<any> {
    return this.http.post(`${this.apiUrl}/get_hsv`, { x, y, image_path: imagePath, remove_image: removeImage });
  }

  getPoints_x01(imagePath: string, tip_down: number, tip_up: number, flight_down: number, flight_up: number): Observable<any> {
    return this.http.post(`${this.apiUrl}/get_points_x01`, { image_path: imagePath, tip_color_down: tip_down, tip_color_up: tip_up, flight_color_down: flight_down, flight_color_up: flight_up });
  }
  
  getPoints_clock(imagePath: string, tip_down: number, tip_up: number, flight_down: number, flight_up: number): Observable<any> {
    return this.http.post(`${this.apiUrl}/get_points_clock`, { image_path: imagePath, tip_color_down: tip_down, tip_color_up: tip_up, flight_color_down: flight_down, flight_color_up: flight_up });
  }

  playerExist(name: any) {
    let data = {
      name: name
    }

    return this.http.post('http://127.0.0.1:4000/dart/playerExist', data)
  }

  playerWins(name: any) {
    let data = {
      name: name
    }

    return this.http.post('http://127.0.0.1:4000/dart/playerWins', data)
  }

  playerExist_clock(name: any) {
    let data = {
      name: name
    }

    return this.http.post('http://127.0.0.1:4000/dart/playerExist_clock', data)
  }

  playerWins_clock(name: any) {
    let data = {
      name: name
    }

    return this.http.post('http://127.0.0.1:4000/dart/playerWins_clock', data)
  }
  
  getPlayers_x01() {
    return this.http.get('http://127.0.0.1:4000/dart/getPlayers_x01')
  }

  getPlayers_clock() {
    return this.http.get('http://127.0.0.1:4000/dart/getPlayers_clock')
  }
}

