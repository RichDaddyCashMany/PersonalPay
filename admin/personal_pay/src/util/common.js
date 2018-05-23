function isInArray (arr, val) {
  for (var i = 0; i < arr.length; i++) {
    if (arr[i] === val) {
      return true
    }
  }
}

function safeJson (json) {
  let dic = json
  for (var key in json) {
    if (json[key] === null || json[key] === undefined) {
      dic[key] = ''
    }
  }
  return dic
}

function safeKeyValueAssign (oldDic, newDic) {
  let dic = oldDic
  for (var key in newDic) {
    if (newDic[key] !== null && newDic[key] !== undefined) {
      dic[key] = newDic[key]
    }
  }
  return dic
}

const common = {
  isInArray: isInArray,
  safeJson: safeJson,
  safeKeyValueAssign
}

export default common
