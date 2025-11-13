#include <iostream>
#include <unordered_map>
#include <vector>
#include <queue>
#include <string>
#include <algorithm>

using namespace std;

bool findpath(unordered_map<string,vector<string>>&graph,string start ,string end,vector<string>&path)
{
    //bfs with list 
    unordered_map<string,bool>visited;
    unordered_map<string,string> parent; // Store parent of each node
    queue<string>q;
    q.push(start);
    visited[start]=true;
    while(!q.empty())
    {
        string current=q.front();
        q.pop();
        
        if(current==end)
        {
            string cur=end;
            while(cur!=start)
            {
                path.push_back(cur);
                cur=parent[cur];
            }
            path.push_back(start);
            reverse(path.begin(),path.end());
            return true; 
        }

        for(string neigh:graph[current])
        {
            if(!visited[neigh])
            {
                q.push(neigh);
                visited[neigh]=true;
                parent[neigh]=current; // Store where we came from
            }
        }
    }
    return false;
}

int main()
{
    bool exit=0;
    while(!exit)
    {
    string start,end;
    cout<<"enter the name of city: ";
    cin>>start;
    cout<<"enter the name of destination: ";
    cin>>end;

    unordered_map<string,vector<string>>graph;
    graph["Delhi"] = {"Jaipur", "Agra","Mumbai"};
    graph["Jaipur"] = {"Delhi", "Udaipur","Agra"};
    graph["Agra"] = {"Delhi", "Kanpur","Udaipur","Jaipur"};
    graph["Udaipur"] = {"Jaipur","Agra","Kanpur"};


    // Europe
    graph["London"] = {"Paris", "Rome"};
    graph["Paris"] = {"London", "Rome"};



    vector<string>path;
    if(findpath(graph,start,end,path))
    {
        cout<<"yes! there is path from "<<start<<"  to  "<<end<<"\n";
        for(int i=0;i<path.size();i++)
        cout<<path[i]<<" ->";
    }
    else 
    {
        cout<<"no route ";
    }
    cout<<endl;
    cout<<"type 1 to exit now ";
    cin>>exit;
    }
    return 0;
}