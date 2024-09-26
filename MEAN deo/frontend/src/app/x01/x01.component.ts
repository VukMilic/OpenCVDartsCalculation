import { Component } from '@angular/core';
import { SlikaHsvService } from '../servers/slika-hsv.service';
import { Router } from '@angular/router';
import { Dart_player_x01 } from '../models/dart_player';

@Component({
  selector: 'app-x01',
  templateUrl: './x01.component.html',
  styleUrls: ['./x01.component.css']
})
export class X01Component {

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
    
    this.imageService.playerExist(this.player1_name).subscribe(((player: Dart_player_x01) => {
      if(player == null){
        this.message = "GRESKA"
      }
    }) as any);
    this.imageService.playerExist(this.player2_name).subscribe(((player: Dart_player_x01) => {
      if(player == null){
        this.message = "GRESKA"
      }
    }) as any);
  }

  imageSrc: string | ArrayBuffer | null = null;
  uploadedImagePath: string = '';

  tip_min_value: number = 0;
  tip_max_value: number = 0;  
  flight_min_value: number = 0;
  flight_max_value: number = 0;

  player1_name: string = 'PLAYER 1';
  player2_name: string = 'PLAYER 2';
  winner: string = '';
  player1_points: number = 501;
  player2_points: number = 501;

  player1_plays: number = 1;
  cnt_plays: number = 0;

  dart_player_1: Dart_player_x01 = new Dart_player_x01;
  dart_player_2: Dart_player_x01 = new Dart_player_x01;

  points: number = 0;

  message: string = "";

  constructor(private imageService: SlikaHsvService, private router: Router){}

  onFileChangeInGame_x01(event: any) {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = e => {
        this.imageSrc = reader.result;  // Display the image
      };
      reader.readAsDataURL(file);

      this.imageService.uploadImage(file).subscribe(response => {
        console.log(response);
        this.uploadedImagePath = response.file_path;
        this.imageService.getPoints_x01(this.uploadedImagePath, this.tip_min_value, this.tip_max_value, this.flight_min_value, this.flight_max_value).subscribe(response=>{
          
          this.points = response.points;
          console.log(`Points gained: ${this.points}`);

          if(this.player1_plays == 1){
            this.player1_points -= this.points;
            if(this.player1_points < 0){
              this.player1_points += this.points;
            }
            else if(this.player1_points == 0){
              this.imageService.playerWins(this.player1_name).subscribe((res: any)=>{
              })
              this.winner = this.player1_name;
              alert(this.winner + " wins!");
              this.router.navigate(['/']);
            }
          }else{
            this.player2_points -= this.points;
            if(this.player2_points < 0){
              this.player2_points += this.points;
            }
            else if(this.player2_points == 0){
              this.imageService.playerWins(this.player2_name).subscribe((res: any)=>{
              })
              this.winner = this.player2_name;
              alert(this.winner + " wins!");
              this.router.navigate(['/']);
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
