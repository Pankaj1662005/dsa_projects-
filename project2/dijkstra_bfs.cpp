#include <iostream>
#include <unordered_map>
#include <vector>
#include <queue>
#include <string>
#include <climits>
#include <algorithm>
using namespace std;

int findmincost(unordered_map<string,vector<pair<string,int>>>&graph,string start,string end)
{
    unordered_map<string,int>cost;
    for(auto p:graph)
    {
        cost[p.first]=INT_MAX;
    }
     // Min-heap stores {cost so far, city name}
    priority_queue<pair<int, string>, vector<pair<int, string>>, greater<pair<int, string>>> pq;
    pq.push({0, start});
    cost[start]=0;
    
    while(!pq.empty())
    {
        auto cur=pq.top();
        pq.pop();

        int currentcost=cur.first;
        string currentcity=cur.second;

        if(currentcity==end)
        {
            return currentcost;
        }

        for(auto e:graph[currentcity])
        {
            string neighbour=e.first;
            int neighbourcost=e.second;
            int newcost=currentcost+neighbourcost;
            if(newcost<cost[neighbour])
            {
                cost[neighbour]=newcost;
                pq.push({newcost,neighbour});
            }
        }
    }

    return -1;


}
int main()
{
    unordered_map<string,vector<pair<string,int>>>graph;
graph["Delhi"] = {{"Jaipur", 100}, {"Agra", 100}, {"Mumbai", 800}, {"Udaipur", 250}, {"Kanpur", 400}};
graph["Jaipur"] = {{"Delhi", 100}, {"Udaipur", 150}, {"Agra", 200}, {"Mumbai", 600}};
graph["Agra"] = {{"Delhi", 100}, {"Kanpur", 350}, {"Jaipur", 200}};
graph["Udaipur"] = {{"Jaipur", 100}, {"Delhi", 250}, {"Kanpur", 600}};
graph["Kanpur"] = {{"Agra", 350}, {"Udaipur", 600}};
graph["Mumbai"] = {{"Delhi", 800}, {"Jaipur", 600}};

// Europe
graph["London"] = {{"Paris", 2}, {"Rome", 3}};
graph["Paris"] = {{"London", 2}, {"Rome", 2}};
graph["Rome"] = {{"London", 3}, {"Paris", 2}};


    string start,end;
    cout<<"enter the start city: ";
    cin>>start;
    cout<<"enter the destination: ";
    cin>>end;

    int mincost=findmincost(graph,start,end);
    if(mincost!=-1)
    {
        cout<<"min cost from "<<start<<" to "<<end<<" will be :"<<mincost<<endl;
    }
    else 
    {
        cout<<"path not found";
    }
    return 0;
}