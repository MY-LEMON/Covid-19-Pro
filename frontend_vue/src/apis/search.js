import axios from "axios";
// import request from '@/utils/request'
export function doSearch(key){
    // return request({
    //     url: '/',
    //     method: 'post',
    //     data: {
    //         key: key
    //     }
    // })
    return axios.get(key)
}


