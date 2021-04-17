import request from '@/utils/request'

export function doSearch(key){
    return request({
        url: '/search',
        method: 'post',
        data: {
            key: key
        }
    })
}

