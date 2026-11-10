#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

static const char *MONTHS[] = {
  "Blossoming","Flurry","Dreaming","Luminary","Sweetening","Sagacity",
  "Gilding","Frigidity","Silvering","Nocturn","Umbery","Emerging","Transition"
};
static const char *DOW[] = {
  "Artemsday","Lunasday","Zeiasday","Daciasday","Athensday","Neosday"
};

static int is_leap(int y){ return (y%4==0 && (y%100!=0 || y%400==0)); }

static int is_leap_luminara(int start_year){
    int y = start_year + 1;
    return is_leap(y);
}

static int month_index(const char *m){
    for(int i=0;i<13;i++) if(strcasecmp(MONTHS[i],m)==0) return i;
    return -1;
}

static void to_luminara(int y,int mo,int da){
    int start_y = y;
    /* adjust if before Apr 20 */
    if (mo < 4 || (mo==4 && da < 20)) start_y--;
    int leap = is_leap_luminara(start_y);
    /* day of year from Apr 20 */
    /* compute days between Apr 20 start_year and date */
    struct tm start = {0}, cur = {0};
    start.tm_year = start_y - 1900; start.tm_mon = 3; start.tm_mday = 20;
    cur.tm_year = y - 1900; cur.tm_mon = mo-1; cur.tm_mday = da;
    time_t ts = mktime(&start), tc = mktime(&cur);
    int doy = (int)((tc-ts)/86400) + 1;
    int lengths[13];
    for(int i=0;i<12;i++) lengths[i]=30;
    lengths[12] = leap ? 6 : 5;
    int acc=0;
    for(int i=0;i<13;i++){
        if(doy <= acc + lengths[i]){
            int dom = doy - acc;
            int n = start_y - 2020;
            const char *era = n<=299?"E1": n<=599?"E2":"E3";
            printf("%s %d, Luminara Year %d %s%s\n", MONTHS[i], dom, n, era, leap?" (leap)":"");
            printf("Weekday: %s\n", DOW[(doy-1)%6]);
            return;
        }
        acc += lengths[i];
    }
}

static void to_gregorian(const char *ms, int day, int year_n){
    if(year_n==0){
        /* default current */
        time_t now=time(NULL); struct tm *t=localtime(&now);
        /* compute current luminara year */
        int sy = t->tm_year+1900;
        if (t->tm_mon < 3 || (t->tm_mon==3 && t->tm_mday < 20)) sy--;
        year_n = sy - 2020;
    }
    int mi = month_index(ms);
    if(mi<0){ fprintf(stderr,"unknown month\n"); exit(1);}
    if(mi==12 && day==6){
        while(!is_leap_luminara(year_n+2020)) year_n++;
    }
    int start_year = year_n + 2020;
    int leap = is_leap_luminara(start_year);
    int lengths[13];
    for(int i=0;i<12;i++) lengths[i]=30;
    lengths[12]=leap?6:5;
    int acc=0; for(int i=0;i<mi;i++) acc+=lengths[i];
    int doy = acc + day;
    struct tm start = {0};
    start.tm_year = start_year - 1900; start.tm_mon=3; start.tm_mday=20;
    time_t ts = mktime(&start);
    time_t tg = ts + (doy-1)*86400;
    struct tm *g = localtime(&tg);
    printf("%s-%d (Year %d) -> %04d-%02d-%02d (%s)\n", MONTHS[mi], day, year_n,
           g->tm_year+1900, g->tm_mon+1, g->tm_mday, g->tm_wday==0?"Sunday":g->tm_wday==1?"Monday":g->tm_wday==2?"Tuesday":g->tm_wday==3?"Wednesday":g->tm_wday==4?"Thursday":g->tm_wday==5?"Friday":"Saturday");
}

int main(int argc, char **argv){
    if(argc==1){
        time_t now=time(NULL); struct tm *t=localtime(&now);
        to_luminara(t->tm_year+1900, t->tm_mon+1, t->tm_mday);
        return 0;
    }
    /* ISO date? */
    if(strchr(argv[1],'-') && strlen(argv[1])==10){
        int y,mo,da;
        if(sscanf(argv[1],"%d-%d-%d",&y,&mo,&da)==3){
            to_luminara(y,mo,da);
            return 0;
        }
    }
    /* to-gregorian subcommand */
    int idx=1;
    if(strcmp(argv[1],"to-gregorian")==0 || strcmp(argv[1],"tg")==0){ idx=2; }
    /* parse month-day (possibly two args) */
    char month[64];
    int day;
    if(strchr(argv[idx],'-')){
        char *dash=strchr(argv[idx],'-');
        size_t len=dash-argv[idx];
        snprintf(month,len+1,"%s",argv[idx]);
        day=atoi(dash+1);
        idx++;
    } else {
        snprintf(month,sizeof month,"%s",argv[idx]);
        day=atoi(argv[idx+1]);
        idx+=2;
    }
    int year_n=0;
    if(idx < argc) year_n=atoi(argv[idx]);
    to_gregorian(month, day, year_n);
    return 0;
}
