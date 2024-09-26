import { Component } from '@angular/core';
import { SlikaHsvService } from '../servers/slika-hsv.service';
import { Router } from '@angular/router';
import { Dart_player_clock } from '../models/dart_player';

@Component({
  selector: 'app-clock',
  templateUrl: './clock.component.html',
  styleUrls: ['./clock.component.css']
})
export class ClockComponent {
  ngOnInit(): void {
    let pom1: any = localStorage.getItem('player1_name');
    if(pom1 != null){
      this.player1_name = pom1
    }
    let pom2: any = localStorage.getItem('player2_name');
    if(pom2 != null){
      this.player2_name = pom2
    }
    let pom3: any = localStorage.getItem('tip_min');
    if(pom3 != null){
      this.tip_min_value = parseInt(pom3)
    }
    let pom4: any = localStorage.getItem('tip_max');
    if(pom4 != null){
      this.tip_max_value = parseInt(pom4)
    }
    let pom5: any = localStorage.getItem('flight_min');
    if(pom5 != null){
      this.flight_min_value = parseInt(pom5)
    }
    let pom6: any = localStorage.getItem('flight_max');
    if(pom6 != null){
      this.flight_max_value = parseInt(pom6)
    }

    this.dart_player_1.name = this.player1_name;
    this.dart_player_2.name = this.player2_name;
    
    this.imageService.playerExist_clock(this.player1_name).subscribe(((player: Dart_player_clock) => {
      if(player == null){
        this.message = "GRESKA"
      }
    }) as any);
    this.imageService.playerExist_clock(this.player2_name).subscribe(((player: Dart_player_clock) => {
      if(player == null){
        this.message = "GRESKA"
      }
    }) as any);
  }

  imageSrc: string | ArrayBuffer | null = null;
  uploadedImagePath: string = '';
  uploadedImageBase64: string = '';

  tip_min_value: number = 0;
  tip_max_value: number = 0;  
  flight_min_value: number = 0;
  flight_max_value: number = 0;

  player1_name: string = 'PLAYER 1';
  player2_name: string = 'PLAYER 2';
  winner: string = '';
  player1_points: number = 1;
  player2_points: number = 1;

  player1_plays: number = 1;
  cnt_plays: number = 0;
  
  points: number = 0;

  dart_player_1: Dart_player_clock = new Dart_player_clock;
  dart_player_2: Dart_player_clock = new Dart_player_clock;

  message: string = "";

  constructor(private imageService: SlikaHsvService, private router: Router){}

  onFileChangeInGame_clock(event: any) {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = e => {
        if(reader.result)
          this.imageSrc = reader.result;  // Display the image
      };
      reader.readAsDataURL(file);

      this.imageService.uploadImage(file).subscribe(response => {
        console.log(response);
        this.uploadedImagePath = response.file_path;
        this.imageService.getPoints_clock(this.uploadedImagePath, this.tip_min_value, this.tip_max_value, this.flight_min_value, this.flight_max_value).subscribe(response=>{
          
          this.points = response.points;
          console.log(`Points gained: ${this.points}`);

          if(this.player1_plays == 1){

            if(this.points == this.player1_points)
              // u slucaju da je pogodjen broj idemo dalje
              switch(this.player1_points){
                case 1:
                  this.player1_points = 18;
                  break;
                case 18:
                  this.player1_points = 4;
                  break;
                case 4:
                  this.player1_points = 13;
                  break;
                case 13:
                  this.player1_points = 6;
                  break;
                case 6:
                  this.player1_points = 10;
                  break;
                case 10:
                  this.player1_points = 15;
                  break;
                case 15:
                  this.player1_points = 2;
                  break;
                case 2:
                  this.player1_points = 17;
                  break;
                case 17:
                  this.player1_points = 3;
                  break;
                case 3:
                  this.player1_points = 19;
                  break;
                case 19:
                  this.player1_points = 7;
                  break;
                case 7:
                  this.player1_points = 16;
                  break;
                case 16:
                  this.player1_points = 8;
                  break;
                case 8:
                  this.player1_points = 11;
                  break;
                case 11:
                  this.player1_points = 14;
                  break;
                case 14:
                  this.player1_points = 9;
                  break;
                case 9:
                  this.player1_points = 12;
                  break;
                case 12:
                  this.player1_points = 5;
                  break;
                case 5:
                  this.player1_points = 20;
                  break;
                case 20:
                  this.imageService.playerWins_clock(this.player1_name).subscribe((res: any)=>{
                  })
                  this.winner = this.player1_name;
                  alert(this.winner + " wins!");
                  this.router.navigate(['/']);    
                  break;
                default:
                  break;
              }
          }else{
            if(this.points == this.player2_points)
              // u slucaju da je pogodjen broj idemo dalje
              switch(this.player2_points){
                case 1:
                  this.player2_points = 18;
                  break;
                case 18:
                  this.player2_points = 4;
                  break;
                case 4:
                  this.player2_points = 13;
                  break;
                case 13:
                  this.player2_points = 6;
                  break;
                case 6:
                  this.player2_points = 10;
                  break;
                case 10:
                  this.player2_points = 15;
                  break;
                case 15:
                  this.player2_points = 2;
                  break;
                case 2:
                  this.player2_points = 17;
                  break;
                case 17:
                  this.player2_points = 3;
                  break;
                case 3:
                  this.player2_points = 19;
                  break;
                case 19:
                  this.player2_points = 7;
                  break;
                case 7:
                  this.player2_points = 16;
                  break;
                case 16:
                  this.player2_points = 8;
                  break;
                case 8:
                  this.player2_points = 11;
                  break;
                case 11:
                  this.player2_points = 14;
                  break;
                case 14:
                  this.player2_points = 9;
                  break;
                case 9:
                  this.player2_points = 12;
                  break;
                case 12:
                  this.player2_points = 5;
                  break;
                case 5:
                  this.player2_points = 20;
                  break;
                case 20:
                  this.imageService.playerWins_clock(this.player2_name).subscribe((res: any)=>{
                  })
                  this.winner = this.player2_name;
                  alert(this.winner + " wins!");
                  this.router.navigate(['/']);    
                  break;
                default:
                  break;
              }
          }
          this.cnt_plays++;
          if(this.cnt_plays == 3){
            this.cnt_plays = 0;
            if(this.player1_plays == 1)
              this.player1_plays = 0
            else
              this.player1_plays = 1
          }
        })
      });
    }
  }

  back(){
    this.router.navigate(['/'])
  }

}
