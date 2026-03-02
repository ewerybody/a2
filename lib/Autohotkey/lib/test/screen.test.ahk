#Requires AutoHotkey v2.0
#Include <screen>

class ScreenTests {
    class VirtualSize {
        width_is_positive() {
            screen_get_virtual_size(&x,&y, &w,&h)
            if w <= 0
                throw Error("Virtual screen width should be positive, got " w)
            if h <= 0
                throw Error("Virtual screen height should be positive, got " h)
            if w < 640
                throw Error("Virtual screen width should be at least 640px, got " w)
        }
    }

    class Workarea {
        width_is_positive() {
            wa := Screen_Workarea()
            if wa.width <= 0
                throw Error("Workarea width should be positive, got " wa.width)
            if wa.height <= 0
                throw Error("Workarea height should be positive, got " wa.height)
            if wa.w != wa.width
                throw Error("wa.w (" wa.w ") should equal wa.width (" wa.width ")")
            if wa.h != wa.height
                throw Error("wa.h (" wa.h ") should equal wa.height (" wa.height ")")
            if wa.x != wa.left
                throw Error("wa.x (" wa.x ") should equal wa.left (" wa.left ")")
            if wa.y != wa.top
                throw Error("wa.y (" wa.y ") should equal wa.top (" wa.top ")")
        }

        right_minus_left_equals_width() {
            wa := Screen_Workarea()
            if wa.right - wa.left != wa.width
                throw Error("right - left should equal width: " wa.right " - " wa.left " != " wa.width)
        }

        bottom_minus_top_equals_height() {
            wa := Screen_Workarea()
            if wa.bottom - wa.top != wa.height
                throw Error("bottom - top should equal height: " wa.bottom " - " wa.top " != " wa.height)
        }
    }

    class WorkareaHelper {
        returns_workarea_object() {
            wa := screen_get_work_area(1)
            if wa.width <= 0 || wa.height <= 0
                throw Error("screen_get_work_area should return a valid workarea")
        }
    }
}
