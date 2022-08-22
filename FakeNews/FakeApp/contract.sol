pragma solidity ^0.4.20;


contract owned {
    address public owner;

    function owned() public {
        owner = msg.sender;
    }

    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    }

    function transferOwnership(address newOwner) onlyOwner public {
        owner = newOwner;
    }
}

contract fightFakeNews is owned{

    uint public sizeORG;
    uint public sizeRealNews;
    uint public gasfee;
    uint newsIDstart;
    uint orgIDstart;

    struct organizations {
        address orgAddress;
        uint orgID;
        string organizationName;
        string orgSource;
        uint[] allArticles;
        bool status;
    }

    struct news {
        uint orgIDforNews;
        string orgNameforNews;
        uint newsID;
        string newsTitle;
        string publisher;
        bool status;
    }

    organizations[] organizationsRecords;
    news[] newRecords;

    // constructor

    function fightFakeNews () public{
        gasfee=0;
        newsIDstart =100000;
        orgIDstart =0;
    }

    // add organizations

    function addOrganization(address _orgAddress, string _organizationName, string _orgsource) public payable returns(uint) {
        require(msg.value==gasfee * 10 ** 15);
        sizeORG = organizationsRecords.length++;
        uint orgIDn;
        orgIDn = orgIDstart++;
        organizationsRecords[organizationsRecords.length-1].orgID = orgIDn;
        organizationsRecords[organizationsRecords.length-1].orgAddress = _orgAddress;
        organizationsRecords[organizationsRecords.length-1].organizationName = _organizationName;
        organizationsRecords[organizationsRecords.length-1].orgSource = _orgsource;
        organizationsRecords[organizationsRecords.length-1].status = true;
        return organizationsRecords.length;
        }

    // Add record by check also the ID (no duplicate IDs)

    function addRealNews(string _newsTitle, string _publisher) public payable returns(uint) {
        require(msg.value==gasfee * 10 ** 15);
        uint index =0;
        bool rights =false;
        for (uint i=0; i<=sizeORG; i++){
            if ((msg.sender==organizationsRecords[i].orgAddress)){
                index=i;
                rights=true;
            }
        }
        require(rights==true);
        require(organizationsRecords[index].status ==true);
        sizeRealNews = newRecords.length++;
        uint newsIDnew;
        newsIDnew = newsIDstart++;
        newRecords[newRecords.length-1].orgNameforNews = organizationsRecords[index].organizationName;
        newRecords[newRecords.length-1].orgIDforNews = organizationsRecords[index].orgID;
        newRecords[newRecords.length-1].newsID = newsIDnew;
        newRecords[newRecords.length-1].newsTitle = _newsTitle;
        newRecords[newRecords.length-1].publisher = _publisher;
        organizationsRecords[index].allArticles.push(newsIDnew);
        newRecords[newRecords.length-1].status = true;
        return organizationsRecords.length;
        }



    // get number of records

    function getOrgRecordsCount() public constant returns(uint) {
        return organizationsRecords.length;
    }

    function getNewsRecordsCount() public constant returns(uint) {
        return newRecords.length;
    }

    // search for news using ID

    function searchNews(uint _searchNews) public constant returns(uint, string, uint, string, string, bool){
    uint index =0;
    for (uint i=0; i<=sizeRealNews; i++){
            if (newRecords[i].newsID == _searchNews){
                index=i;
            }
        }

    return (newRecords[index].orgIDforNews, newRecords[index].orgNameforNews, newRecords[index].newsID, newRecords[index].newsTitle, newRecords[index].publisher, newRecords[index].status);
    }

    // search for org using ID

    function searchORG(uint _seachOrg) public constant returns(address, uint, string, string, bool){
    uint index =0;
    for (uint i=0; i<=sizeORG; i++){
            if (organizationsRecords[i].orgID == _seachOrg){
                index=i;
            }
        }

    return (organizationsRecords[index].orgAddress, organizationsRecords[index].orgID, organizationsRecords[index].organizationName, organizationsRecords[index].orgSource, organizationsRecords[index].status);
    }

    // return table

    // search for org using ID

    function returnORGarraywithNews(uint _seachOrg) public constant returns(uint[]){
    uint index =0;
    for (uint i=0; i<=sizeORG; i++){
            if (organizationsRecords[i].orgID == _seachOrg){
                index=i;
            }
        }

    return (organizationsRecords[index].allArticles);
    }



    // Advanced functions

    // change status of News

    function changeStatusofNews(uint _newsID, bool _revokestatus) public payable{
    require(msg.sender==owner);
        uint index =0;
        for (uint i=0; i<=sizeRealNews; i++){
            if (newRecords[i].newsID == _newsID){
                index=i;
            }
        }
    newRecords[index].status=_revokestatus;

    }

    // changes status of Org

    function changeStatusofORGs(uint _orgID, bool _revokestatus) public payable{
    require(msg.sender==owner);
        uint index =0;
        for (uint i=0; i<=sizeORG; i++){
            if (organizationsRecords[i].orgID == _orgID){
                index=i;
            }
        }
    organizationsRecords[index].status=_revokestatus;

    }

}
