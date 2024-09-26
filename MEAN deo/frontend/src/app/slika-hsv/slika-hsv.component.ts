import { Component } from '@angular/core';
import { SlikaHsvService } from '../servers/slika-hsv.service';
import { Router } from '@angular/router';
import { Dart_player_clock, Dart_player_x01 } from '../models/dart_player';

@Component({
  selector: 'app-slika-hsv',
  templateUrl: './slika-hsv.component.html',
  styleUrls: ['./slika-hsv.component.css']
})
export class SlikaHsvComponent {

  ngOnInit(): void {
    this.imageService.getPlayers_clock().subscribe(((players: Dart_player_clock[])=>{
      if(players != null){
        this.dart_clock_players = players;
        this.dart_clock_players.sort(this.sortWins);
      }
    }) as any);
    this.imageService.getPlayers_x01().subscribe(((players: Dart_player_x01[])=>{
      if(players != null){
        this.dart_x01_players = players;
        this.dart_x01_players.sort(this.sortWins);
      }
    }) as any);
  }

  imageSrc: string | ArrayBuffer | null = null;
  hsvValue: number[] = [0, 0, 0];
  uploadedImagePath: string = '';
  clickCnt: number = 0;

  bPlay = 0;
  bStart = 0;
  bStarted = 0;

  tip_color_values: number[] = [0, 0, 0];
  flight_color_values: number[] = [0, 0, 0];

  tip_min_value: number = 0;
  tip_max_value: number = 0;  
  flight_min_value: number = 0;
  flight_max_value: number = 0;

  images_123 = 0;

  player1_name: string = '';
  player2_name: string = '';
  player1_points: number = 501;
  player2_points: number = 501;

  player1_plays: number = 1;

  points: number = 0;

  dart_x01_players: Dart_player_x01[] = [];
  dart_clock_players: Dart_player_clock[] = [];
  

  constructor(private imageService: SlikaHsvService, private router: Router) {}

  sortWins(a: any, b: any) {
    if (a.wins < b.wins) {
      return 1;
    } else {
      return -1;
    }
  }

  onFileChange1(event: any) {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = e => {
        this.imageSrc = reader.result;  // Display the image
      };
      reader.readAsDataURL(file);
      
      this.images_123 = 1;

      this.imageService.uploadImage(file).subscribe(response => {
        console.log(response);
        this.uploadedImagePath = response.file_path; // Store file path for later use
      });
    }
  }

  onFileChange2(event: any) {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = e => {
        this.imageSrc = reader.result;  // Display the image
      };
      reader.readAsDataURL(file);

      this.images_123 = 2;

      this.imageService.uploadImage(file).subscribe(response => {
        console.log(response);
        this.uploadedImagePath = response.file_path; // Store file path for later use
      });
    }
  }

  onFileChange3(event: any) {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = e => {
        this.imageSrc = reader.result;  // Display the image
      };
      reader.readAsDataURL(file);

      this.images_123 = 3;

      this.imageService.uploadImage(file).subscribe(response => {
        console.log(response);
        this.uploadedImagePath = response.file_path; // Store file path for later use
      });
    }
  }

  getHSV(event: MouseEvent) {
    const rect = (event.target as HTMLImageElement).getBoundingClientRect();
    const x = event.clientX - rect.left; // Get mouse X coordinate
    const y = event.clientY - rect.top;  // Get mouse Y coordinate
    let removeImage = 0;
    if(this.clickCnt%2 == 1){
      removeImage = 1;
    }
    this.imageService.getHSV(x, y, this.uploadedImagePath, removeImage).subscribe(response => {
      this.hsvValue = response.hsv_value;
      console.log(`HSV Value at (${x}, ${y}): `, this.hsvValue);
      this.clickCnt++;
      if(this.clickCnt == 1 || this.clickCnt == 3 || this.clickCnt == 5){
        for( let i=0; i<3 ; i++){
          if(this.flight_color_values[i] == 0){
            this.flight_color_values[i] = this.hsvValue[0];
            break;
          }
        }
      }
      else if(this.clickCnt == 2 || this.clickCnt == 4){
        for( let i=0; i<2; i++){
          if(this.tip_color_values[i] == 0){
            this.tip_color_values[i] = this.hsvValue[0];
            break;
          }
        }
        this.imageSrc = null;
      }
      else if(this.clickCnt == 6){
        this.tip_color_values[2] = this.hsvValue[0];
        
        // sada imamo po tri vrednosti u oba niza
        // potrebno je da izvucemo najmanju i najvecu vrednost iz oba niza
        // i da dodamo i oduzmemo 5 u sve cetiri vrednosti
        this.tip_min_value = Math.min(...this.tip_color_values)
        this.tip_min_value = this.tip_min_value - 5;
        this.tip_max_value = Math.max(...this.tip_color_values)
        this.tip_max_value = this.tip_max_value + 5;

        this.flight_min_value = Math.min(...this.flight_color_values)
        this.flight_min_value = this.flight_min_value - 5;
        this.flight_max_value = Math.max(...this.flight_color_values)
        this.flight_max_value = this.flight_max_value + 5;

        this.imageSrc = null;
        this.bStart = 1;
      }
    });
  }

  play(){
    this.bPlay = 1;
    if(this.player1_name == ''){
      this.player1_name = 'PLAYER 1'
    }
    if(this.player2_name == ''){
      this.player2_name = 'PLAYER 2'
    }
  }

  back(){
    this.bPlay = 0;
    if(this.player1_name == 'PLAYER 1'){
      this.player1_name = ''
    }
    if(this.player2_name == 'PLAYER 2'){
      this.player2_name = ''
    }
  }

  reset(){
    this.bStart = 0;
    this.clickCnt = 0;
    this.imageSrc = null;
    this.hsvValue = [0, 0, 0];
    this.images_123 = 0;
    this.uploadedImagePath = '';

    this.tip_color_values = [0, 0, 0];
    this.flight_color_values = [0, 0, 0];

    this.tip_min_value = 0;
    this.tip_max_value = 0;  
    this.flight_min_value = 0;
    this.flight_max_value = 0;

    this.bPlay = 1;
    this.bStart = 0;
    this.bStarted = 0;
  }

  start_x01(){
    localStorage.setItem("player1_name", this.player1_name)
    localStorage.setItem("player2_name", this.player2_name)
    localStorage.setItem("tip_min", this.tip_min_value.toString())
    localStorage.setItem("tip_max", this.tip_max_value.toString())
    localStorage.setItem("flight_min", this.flight_min_value.toString())
    localStorage.setItem("flight_max", this.flight_max_value.toString())
    
    this.router.navigate(['/x01'])
  }
  start_cicket(){

  }
  start_clock(){
    localStorage.setItem("player1_name", this.player1_name)
    localStorage.setItem("player2_name", this.player2_name)
    localStorage.setItem("tip_min", this.tip_min_value.toString())
    localStorage.setItem("tip_max", this.tip_max_value.toString())
    localStorage.setItem("flight_min", this.flight_min_value.toString())
    localStorage.setItem("flight_max", this.flight_max_value.toString())
    
    this.router.navigate(['/clock'])
  }

}
