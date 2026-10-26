p='engine-src/prboom2/src/g_game.c'
s=open(p).read()
code=r'''
/* Race simulator interface: read-only observation plus vanilla ticcmd input. */
static void RaceInput(ticcmd_t *cmd) {
 static FILE *in = NULL, *out = NULL;
 player_t *p = &players[0]; mobj_t *m = p->mo; thinker_t *th;
 int i, first = 1, f, side, a, b;
 if (!in) { out=fopen(getenv("RACE_OUT"),"w"); in=fopen(getenv("RACE_IN"),"r"); }
 fprintf(out,"{\"tic\":%d,\"map\":%d,\"state\":%d,\"x\":%.6f,\"y\":%.6f,\"z\":%.6f,\"angle\":%u,\"vx\":%.6f,\"vy\":%.6f,\"health\":%d,\"armor\":%d,\"weapon\":%d,\"kills\":%d,\"sector\":%ld,\"ammo\":[",leveltime,gamemap,gamestate,m->x/65536.,m->y/65536.,m->z/65536.,m->angle,m->momx/65536.,m->momy/65536.,p->health,p->armorpoints[0],p->readyweapon,p->killcount,(long)(m->subsector->sector-sectors));
 for(i=0;i<4;i++)fprintf(out,"%s%d",i?",":"",p->ammo[i]);
 fprintf(out,"],\"keys\":[");for(i=0;i<6;i++)fprintf(out,"%s%d",i?",":"",p->cards[i]);
 fprintf(out,"],\"owned\":[");for(i=0;i<9;i++)fprintf(out,"%s%d",i?",":"",p->weaponowned[i]);
 fprintf(out,"],\"sectors\":[");for(i=0;i<numsectors;i++)fprintf(out,"%s[%g,%g]",i?",":"",sectors[i].floorheight/65536.,sectors[i].ceilingheight/65536.);
 fprintf(out,"],\"monsters\":[");
 for(th=thinkercap.next;th!=&thinkercap;th=th->next) if(th->function==P_MobjThinker) {
  mobj_t *o=(mobj_t*)th;
  if(o!=m && (o->flags & (MF_SHOOTABLE|MF_MISSILE|MF_SPECIAL))) {
   fprintf(out,"%s[%d,%.4f,%.4f,%.4f,%d,%lu,%u]",first?"":",",o->type,o->x/65536.,o->y/65536.,o->z/65536.,o->health,(unsigned long)o->flags,o->angle);first=0;
  }
 }
 fprintf(out,"]}\n");fflush(out);
 if(fscanf(in,"%d %d %d %d",&f,&side,&a,&b)!=4) exit(0);
 memset(cmd,0,sizeof(*cmd));cmd->forwardmove=f;cmd->sidemove=side;cmd->angleturn=a*256;cmd->buttons=b;
}
'''
s=s.replace('// Allows use of HELP2 screen',code+'\n// Allows use of HELP2 screen')
s=s.replace('if (demoplayback)\n          dsda_TryPlaybackOneTick(cmd);','if (demoplayback) {\n          if(getenv("RACE_IN")) RaceInput(cmd);\n          else dsda_TryPlaybackOneTick(cmd);\n        }')
open(p,'w').write(s)
