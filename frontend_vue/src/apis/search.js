import request from '@/utils/request'

export function doSearch(key){
    return request({
        url: '/',
        method: 'post',
        data: {
            key: key
        }
    })
}


