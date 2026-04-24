#include "Object.h"
#include "Splash.h"

Dir DIRE[4]={
	{-1,0,UP},
	{1,0,DOWN},
	{0,-1,LEFT},
	{0,1,RIGHT}
};
string STR[5]={"","LEFT","RIGHT","UP","DOWN"};

Water::Water(int val,int mx,int my,Splash* msplash){
    value=val,x=mx,y=my,splash=msplash;
}
int Water::act(Direction fromwhere, Actor fromwho){
    cout << "现在是 WATER " << x << ' ' << y << "\n";
    if(fromwho==PLAYER) return act(fromwhere,WATER);
    if(fromwho==WATER){
        
        if((++value)<=3) return 0;
        splash->map[x][y]=new Void(x,y,splash);
        cout << "WATER " << x << ' ' << y << " 爆了\n";
        for(int i=0;i<4;i++){
            int tx=x+DIRE[i].x,ty=y+DIRE[i].y;
            
            if(tx >=0 && tx < splash->size && ty>=0 && ty< splash->size){
                cout << "WATER " << x << ' ' << y << " 爆 " << tx << ' ' << ty << '\n';
                Object *obj=splash->map[tx][ty];
                obj->act(DIRE[i].dir,WATER);
                cout << "WATER " << x << ' ' << y << " 爆 " << tx << ' ' << ty << "结束\n";
                if(obj != splash->map[x][y]) delete obj;
            }
        }

        
        return 1;
    }
    if(fromwho==TOXIC){
        --value;
        if(value==0) splash->map[x][y]=new Void(x,y,splash);
        return 0;
    }

}

Toxic::Toxic(int val,int mx,int my,Splash* msplash){
    value=val,x=mx,y=my,splash=msplash;
}
int Toxic::act(Direction fromwhere, Actor fromwho){
    if(fromwho==PLAYER) return act(fromwhere,TOXIC);
    if(fromwho==WATER){
        cout << "TOXIC " << x << ' ' << y << " 得水 " << '\n';
        ++value;
        if(value==0) splash->map[x][y]=new Void(x,y,splash);
        return 0;
    }
    if(fromwho==TOXIC){
        if((--value)>=-3) return 0;
        splash->map[x][y]=new Void(x,y,splash);
        for(int i=0;i<4;i++){
            int tx=x+DIRE[i].x,ty=y+DIRE[i].y;
            if(tx >=0 && tx < splash->size && ty>=0 && ty< splash->size){
                Object *obj=splash->map[tx][ty];
                obj->act(DIRE[i].dir,TOXIC);
                if(obj != splash->map[x][y]) delete obj;
            }
        }
        return -1;
    }

}

Void::Void(int mx,int my,Splash* msplash){
    x=mx,y=my,splash=msplash;
}
int Void::act(Direction fromwhere, Actor fromwho){
    if(fromwho==PLAYER) cout << "Error: Cannot act a Void.\n";
    else{
        cout << "Void " << x << ' ' << y << " 路过 " << '\n';
        for(int i=0;i<4;i++){
            int tx=x+DIRE[i].x,ty=y+DIRE[i].y;
            if(fromwhere==DIRE[i].dir && tx >=0 && tx < splash->size &9& ty>=0 && ty< splash->size){
                cout << "Void " << x << ' ' << y << " 方向 " << STR[fromwhere] << '\n';
                Object *obj=splash->map[tx][ty];
                obj->act(DIRE[i].dir,fromwho);
                if(obj != splash->map[x][y]) delete obj;
                break;
            }
        }
    }
    return 0;
}

Barrier::Barrier(int mx,int my,Splash* msplash){
    x=mx,y=my,splash=msplash;
}
int Barrier::act(Direction fromwhere, Actor fromwho){
    if(fromwho==PLAYER) cout << "Error: Cannot act a Barrier.\n";
    return 0;
}