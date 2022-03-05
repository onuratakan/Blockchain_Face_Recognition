// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.7.0 <0.9.0;


contract Storage {

    string yazi;

    function store(string memory _yazi) public {
        yazi = _yazi;
    }

    function retrieve() public view returns (string memory){
        return yazi;
    }
}
