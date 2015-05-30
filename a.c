#include<stdio.h>
#include<string.h>
main(){
    int i,j,k;
    char command[300] = {0,};
    for(i=0;i<2;i++){
    for(j=0;j<2;j++){
    for(k=0;k<2;k++){
        printf("%d %d %d\n", i,j,k);
        snprintf(command, 300, "python hij_matching.py male.csv %d %d %d > results/stat_male_%d%d%d.txt", i,j,k,i,j,k);
        system(command);
        snprintf(command, 300, "python hij_matching.py female.csv %d %d %d > results/stat_female_%d%d%d.txt", i,j,k,i,j,k);
        system(command);
    }
    }
    }
}
