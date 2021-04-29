// import request from '@/utils/request'
//
// export function doSearch(key){
//     return request({
//         url: '/',
//         method: 'post',
//         data: {
//             key: key
//         }
//     })
// }
//
//
import axios from "axios";

export function doSearch(key){
    return axios.get('https://bdc51f09-c370-4318-9d0d-5cacb9fa267f.mock.pstmn.io/'+key)
}
