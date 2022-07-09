potato_host="https://www.potatomedia.co"
login_url=f"{potato_host}/auth/signin"
latest_post_url=f"{potato_host}/posts/latest"
reg = "https://www.potatomedia.co/post/([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})"

contexts ="""
至於為什麼要思考呢？其實是有更深層的原因，更多的意義是這樣的，歌德有講過一句名言，決定一個人的一生，以及整個命運的，只是一瞬之間。這不禁令我深思。維龍有說過一句話，要成功不需要什麽特別的才能，只要把你能做的小事做得好就行了。這句話語雖然很短，但令我浮想聯翩。史美爾斯有講過一句名言，書籍把我們引入最美好的社會，使我們認識各個時代的偉大智者。這讓我思索了許久，總結的來說，問題的關鍵究竟為何？而這些並不是完全重要，更加重要的問題是，帶著這些問題，我們來審視一下。一般來說，為什麼是這樣呢？在這種困難的抉擇下，本人思來想去，寢食難安。
"""

draft_info = {
    "title": "廢文",
    "contents": contexts
}

ex_uuid = [
    "98a2ef8d-60fe-42e1-8c67-346f2219be19",
    "ae0cd8fe-0955-43c4-85ac-c0b77828e54a",
    "f146194f-1a7b-422a-9643-4538bf882d13"]