#include <iostream>
#include<vector>
#include<algorithm>
#include<set>
using namespace std;
int main()
{
    // 请在此输入您的代码
    int n,k;
    cin>>n>>k;
    vector<int> v,ans;
    for(int i=0;i<n;i++){
        int a;
        cin>>a;
        v.push_back(a);
    }
    //int num=0;
    set<vector<int>> s;
    for(int j=1;j<=n;j++){
        for(int i=0;i<n;i++){
            int a=0;
            for(int l=i;l<min(i+j,n);l++){
                a+=v[l];
                //cout<<a<<" ";
                ans.push_back(v[l]);
            }
            cout<<endl;
            if(a%k==0){
                //num++;
                s.insert(ans);
                for (int l=0;l<ans.size();l++) {
                    cout<<ans[l]<<" ";
                }
                cout<<endl;
            }
            ans.clear();

        }
    }
    cout<<s.size();
    return 0;
}